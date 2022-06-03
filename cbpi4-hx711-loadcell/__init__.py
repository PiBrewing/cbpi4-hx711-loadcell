
# -*- coding: utf-8 -*-
import os
from aiohttp import web
import logging
import RPi.GPIO as GPIO
from unittest.mock import MagicMock, patch
import asyncio
import random
from cbpi.api import *
import time
from cbpi.api.timer import Timer
from .hx711 import HX711
from cbpi.api.dataclasses import NotificationAction, NotificationType

logger = logging.getLogger(__name__)


@parameters([Property.Select(label="dout", options=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27], description="GPIO Pin connected to the Serial Data Output Pin of the HX711"),
    Property.Select(label="pd_sck", options=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27], description="GPIO Pin connected to the Power Down & Seerial Clock Pin of the HX711"),
    Property.Select(label="gain", options = [128,64, 32],description = "Select gain for HX711"),
    Property.Number(label="offset",configurable = True, default_value = 0, description="Offset for the HX711 scale from callibration setup (Default is 0)"),
    Property.Number(label="scale",configurable = True, default_value = 0, description="Scale ratio input for the HX711 scale from callibration setup (Default is 1)"),
    Property.Select(label="Interval", options=[1,2,5,10,30,60], description="Interval in Seconds")])

class CustomSensor(CBPiSensor):


    def __init__(self, cbpi, id, props):
        super(CustomSensor, self).__init__(cbpi, id, props)
        self.value = 0
        self.dout = int(self.props.get("dout",27))
        self.pd_sck = int(self.props.get("pd_sck",23))
        self.gain = int(self.props.get("gain",128))
        self.Interval = int(self.props.get("Interval",2))
        self.offset = int(self.props.get("offset",0))
        self.scale = int(self.props.get("scale",1))
        self.calibration_active = False
        self.measurement_is_running = False

        logging.info("INIT HX711:")
        logging.info("dout: {}".format(self.dout))
        logging.info("pd_sck: {}".format(self.pd_sck))
        logging.info("gain: {}".format(self.gain))
        logging.info("offset: {}".format(self.offset))
        logging.info("scale: {}".format(self.scale))

    @action(key="Tare Sensor", parameters=[])
    async def Reset(self, **kwargs):
        self.hx.tare()
        logging.info("Tare HX711 Loadcell")

    @action(key="Calibrate Sensor", parameters=[Property.Number(label="weight",configurable=True, default_value = 0, description="Please enter the known weight of your calibration item and remove all weight from your scale")])
    async def Calibrate(self ,weight = 0, **kwargs):
        self.next = False
        self.weight = float(weight)
        if self.weight <= 0:
            self.cbpi.notify("Loadcell Calibration Error", "Weight for calibration must be larger than 0", NotificationType.ERROR, action=[NotificationAction("Next", self.NextStep)])
            return
        logging.info(weight)
        self.calibration_active = True
        while self.measurement_is_running is not False:
            logging.info("Waiting for Sensor")
            await asyncio.sleep(self.Interval)
            pass
        self.hx.set_offset(0)
        self.hx.set_reference_unit(1)
        logging.info("Reset")
        await self.hx.reset()
        await asyncio.sleep(1)
        logging.info("Calibrate HX711 Loadcell")
        self.cal_offset = self.hx.read_average()
        logging.info("Offset {}".format(self.cal_offset))
        self.cbpi.notify("Loadcell Calibration", "Please put your known weight on the scale and press next", NotificationType.INFO, action=[NotificationAction("Next Step", self.NextStep)])
        while not self.next == True:
            await asyncio.sleep(1)
            pass
        self.next = False

        self.reading = self.hx.read_average()
        self.calibration_factor = round(((self.reading-self.cal_offset) / self.weight),1)
        logging.info("Scale Factor {}".format(self.calibration_factor))
        self.cbpi.notify("Loadcell Calibration done", "Enter these values in the sensor hardware. Offset: {}; Scale: {}".format(self.cal_offset, self.calibration_factor),action=[NotificationAction("Next Step", self.NextStep)])
        while not self.next == True:
            await asyncio.sleep(1)
            pass
        self.next = False

        logging.info("Set Offset")
        self.hx.set_offset(self.offset)
        logging.info("Set Reference Unit")
        self.hx.set_reference_unit(self.scale)
        logging.info("Reset")
        await self.hx.reset()
        await asyncio.sleep(1)
        logging.info("Tare")
        self.hx.tare()
        self.calibration_active = False

    async def NextStep(self):
        self.next = True
        pass

    async def run(self):

        logging.info("Setup HX711")
        self.hx = HX711(self.dout, self.pd_sck, self.gain)
        logging.info("Set Reading Format")
        self.hx.set_reading_format("MSB", "MSB")
        logging.info("Set Offset")
        self.hx.set_offset(self.offset)
        logging.info("Set Reference Unit")
        self.hx.set_reference_unit(self.scale)
        logging.info("Reset")
        await self.hx.reset()
        await asyncio.sleep(1)
        logging.info("Tare")
        self.hx.tare()

        while self.running is True:
            try:
                if self.calibration_active == False:
                    self.measurement_is_running = True
                    self.value = round(self.hx.get_weight(5),2)
                    await self.hx.power_down()
                    await asyncio.sleep(.001)
                    await self.hx.power_up()
                    self.log_data(self.value)
                    self.push_update(self.value)
                    self.measurement_is_running = False
                    await asyncio.sleep(self.Interval)
                else:
                    await asyncio.sleep(self.Interval)
                    pass
            except:
                await asyncio.sleep(self.Interval)
                pass

    def get_state(self):
        return dict(value=self.value)

@parameters([Property.Number(label="Weight", description="Number of L to Tranfer", configurable=True),
             Property.Number(label="Density", description="Expected Wort Density - 1.XXX <-> 1.2", configurable=True),
             Property.Select(label="useDensity",options=["Yes","No"], description="Use Density Offset within this Step"),
             Property.Actor(label="Actor",description="Actor to switch media flow on and off"),
             Property.Sensor(label="Sensor"),
             Property.Select(label="Reset", options=["Yes","No"],description="Tare Weight when done")])

class WeightStep(CBPiStep):

    async def on_timer_done(self,timer):
        self.summary = ""
        self.cbpi.notify(self.name, 'Step finished. Transferred {} {}.'.format(round(self.current_volume,2),'L'), NotificationType.SUCCESS)
       # if self.resetsensor == "Yes":
      #      self.sensor.instance.hx.tare()

        if self.actor is not None:
            await self.actor_off(self.actor)
        await self.next()

    async def on_timer_update(self,timer, seconds):
        await self.push_update()

    async def on_start(self):
        self.actor = self.props.get("Actor", None)
        self.target_volume = float(self.props.get("Weight",0))
        self.flowsensor = self.props.get("Sensor",None)
        logging.info(self.flowsensor)
        self.sensor = self.get_sensor(self.flowsensor)
        logging.info(self.sensor)
        self.resetsensor = self.props.get("Reset","Yes")
        self.dens_flag = True if self.props.get("useDensity", "No") == "Yes" else False
        self.density = float(self.props.get("Density",0))

        #CustomSensor.self.hx.tare()
        if self.timer is None:
            self.timer = Timer(1,on_update=self.on_timer_update, on_done=self.on_timer_done)

    async def on_stop(self):
        if self.timer is not None:
            await self.timer.stop()
        self.summary = ""
        if self.actor is not None:
            await self.actor_off(self.actor)
        await self.push_update()

    async def reset(self):
        self.timer = Timer(1,on_update=self.on_timer_update, on_done=self.on_timer_done)
        if self.actor is not None:
            await self.actor_off(self.actor)


    async def run(self):
        if self.actor is not None:
            await self.actor_on(self.actor)
        self.summary=""
        await self.push_update()
        while self.running == True:

            self.current_volume = self.get_sensor_value(self.flowsensor).get("value") * self.density if self.dens_flag == True else self.get_sensor_value(self.flowsensor).get("value")
            self.summary="Volume: {}".format(self.current_volume)
         #   self.cbpi.notify("WaterTransfer","Current: {}L, Target {}L".format(self.current_volume,self.target_volume), NotificationType.INFO)
            await self.push_update()

            if self.current_volume >= self.target_volume and self.timer.is_running is not True:
                self.timer.start()
                self.timer.is_running = True

            await asyncio.sleep(0.2)

        return StepResult.DONE



def setup(cbpi):
    cbpi.plugin.register("HX711 Load Cell", CustomSensor)
    cbpi.plugin.register("WeightStep", WeightStep)
    pass
