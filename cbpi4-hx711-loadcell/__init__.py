
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
from HX711 import *
from cbpi.api.dataclasses import NotificationAction, NotificationType
from cbpi.api.config import ConfigType

logger = logging.getLogger(__name__)

class HX711_Config(CBPiExtension):
    def __init__(self,cbpi):
        self.cbpi = cbpi
        self._task = asyncio.create_task(self.init_sensor())


    async def init_sensor(self):
        plugin = await self.cbpi.plugin.load_plugin_list("cbpi4-hx711-loadcell")
        self.version=plugin[0].get("Version","0.0.0")
        self.name=plugin[0].get("Name","cbpi4-hx711-loadcell")

        self.hx711_update = self.cbpi.config.get(self.name+"_update", None)

        await self.HX711_settings()
        
        self.dout = self.cbpi.config.get("HX711_dout", 5)
        self.sck = self.cbpi.config.get("HX711_sck", 6)
        global hx 
        hx=SimpleHX711(self.dout, self.sck)

    async def HX711_settings(self):
        global HX711_dout
        global HX711_sck
        HX711_dout = self.cbpi.config.get("HX711_dout", None)
        if HX711_dout is None:
            logger.info("INIT HX711_dout")
            try:
                await self.cbpi.config.add("HX711_dout", 5, type=ConfigType.SELECT, description="HX711 dout GPIO",
                                                                                                    source=self.name,
                                                                                        options=[{"label": "0", "value": 0},
                                                                                                {"label": "1", "value": 1},
                                                                                                {"label": "2", "value": 2},
                                                                                                {"label": "3", "value": 3},
                                                                                                {"label": "4", "value": 4},
                                                                                                {"label": "5", "value": 5},
                                                                                                {"label": "6", "value": 6},
                                                                                                {"label": "7", "value": 7},
                                                                                                {"label": "8", "value": 8},
                                                                                                {"label": "9", "value": 9},
                                                                                                {"label": "10", "value": 10},
                                                                                                {"label": "11", "value": 11},
                                                                                                {"label": "12", "value": 12},
                                                                                                {"label": "13", "value": 13},
                                                                                                {"label": "14", "value": 14},
                                                                                                {"label": "15", "value": 15},
                                                                                                {"label": "16", "value": 16},
                                                                                                {"label": "17", "value": 17},
                                                                                                {"label": "18", "value": 18},
                                                                                                {"label": "19", "value": 19},
                                                                                                {"label": "20", "value": 20},
                                                                                                {"label": "21", "value": 21},
                                                                                                {"label": "22", "value": 22},
                                                                                                {"label": "23", "value": 23},
                                                                                                {"label": "24", "value": 24},
                                                                                                {"label": "25", "value": 25},
                                                                                                {"label": "26", "value": 26},
                                                                                                {"label": "27", "value": 27}])
                                                                                                            
                HX711_dout = self.cbpi.config.get("HX711_dout", None)
            except:
                logger.warning('Unable to update database')
        else:
            if self.hx711_update == None or self.hx711_update != self.version:
                try:
                    await self.cbpi.config.add("HX711_dout", HX711_dout, type=ConfigType.SELECT, description="HX711 dout GPIO",
                                                                                                    source=self.name,
                                                                                        options=[{"label": "0", "value": 0},
                                                                                                {"label": "1", "value": 1},
                                                                                                {"label": "2", "value": 2},
                                                                                                {"label": "3", "value": 3},
                                                                                                {"label": "4", "value": 4},
                                                                                                {"label": "5", "value": 5},
                                                                                                {"label": "6", "value": 6},
                                                                                                {"label": "7", "value": 7},
                                                                                                {"label": "8", "value": 8},
                                                                                                {"label": "9", "value": 9},
                                                                                                {"label": "10", "value": 10},
                                                                                                {"label": "11", "value": 11},
                                                                                                {"label": "12", "value": 12},
                                                                                                {"label": "13", "value": 13},
                                                                                                {"label": "14", "value": 14},
                                                                                                {"label": "15", "value": 15},
                                                                                                {"label": "16", "value": 16},
                                                                                                {"label": "17", "value": 17},
                                                                                                {"label": "18", "value": 18},
                                                                                                {"label": "19", "value": 19},
                                                                                                {"label": "20", "value": 20},
                                                                                                {"label": "21", "value": 21},
                                                                                                {"label": "22", "value": 22},
                                                                                                {"label": "23", "value": 23},
                                                                                                {"label": "24", "value": 24},
                                                                                                {"label": "25", "value": 25},
                                                                                                {"label": "26", "value": 26},
                                                                                                {"label": "27", "value": 27}])
                except:
                    logger.warning('Unable to update database')

        HX711_sck = self.cbpi.config.get("HX711_sck", None)
        if HX711_dout is None:
            logger.info("INIT HX711_sck")
            try:
                await self.cbpi.config.add("HX711_sck", 6, type=ConfigType.SELECT, description="HX711 sck GPIO",
                                                                                                    source=self.name,
                                                                                        options=[{"label": "0", "value": 0},
                                                                                                {"label": "1", "value": 1},
                                                                                                {"label": "2", "value": 2},
                                                                                                {"label": "3", "value": 3},
                                                                                                {"label": "4", "value": 4},
                                                                                                {"label": "5", "value": 5},
                                                                                                {"label": "6", "value": 6},
                                                                                                {"label": "7", "value": 7},
                                                                                                {"label": "8", "value": 8},
                                                                                                {"label": "9", "value": 9},
                                                                                                {"label": "10", "value": 10},
                                                                                                {"label": "11", "value": 11},
                                                                                                {"label": "12", "value": 12},
                                                                                                {"label": "13", "value": 13},
                                                                                                {"label": "14", "value": 14},
                                                                                                {"label": "15", "value": 15},
                                                                                                {"label": "16", "value": 16},
                                                                                                {"label": "17", "value": 17},
                                                                                                {"label": "18", "value": 18},
                                                                                                {"label": "19", "value": 19},
                                                                                                {"label": "20", "value": 20},
                                                                                                {"label": "21", "value": 21},
                                                                                                {"label": "22", "value": 22},
                                                                                                {"label": "23", "value": 23},
                                                                                                {"label": "24", "value": 24},
                                                                                                {"label": "25", "value": 25},
                                                                                                {"label": "26", "value": 26},
                                                                                                {"label": "27", "value": 27}])
                                                                                                            
                HX711_sck = self.cbpi.config.get("HX711_sck", None)
            except:
                logger.warning('Unable to update database')
        else:
            if self.hx711_update == None or self.hx711_update != self.version:
                try:
                    await self.cbpi.config.add("HX711_sck", HX711_sck, type=ConfigType.SELECT, description="HX711 sck GPIO",
                                                                                                    source=self.name,
                                                                                        options=[{"label": "0", "value": 0},
                                                                                                {"label": "1", "value": 1},
                                                                                                {"label": "2", "value": 2},
                                                                                                {"label": "3", "value": 3},
                                                                                                {"label": "4", "value": 4},
                                                                                                {"label": "5", "value": 5},
                                                                                                {"label": "6", "value": 6},
                                                                                                {"label": "7", "value": 7},
                                                                                                {"label": "8", "value": 8},
                                                                                                {"label": "9", "value": 9},
                                                                                                {"label": "10", "value": 10},
                                                                                                {"label": "11", "value": 11},
                                                                                                {"label": "12", "value": 12},
                                                                                                {"label": "13", "value": 13},
                                                                                                {"label": "14", "value": 14},
                                                                                                {"label": "15", "value": 15},
                                                                                                {"label": "16", "value": 16},
                                                                                                {"label": "17", "value": 17},
                                                                                                {"label": "18", "value": 18},
                                                                                                {"label": "19", "value": 19},
                                                                                                {"label": "20", "value": 20},
                                                                                                {"label": "21", "value": 21},
                                                                                                {"label": "22", "value": 22},
                                                                                                {"label": "23", "value": 23},
                                                                                                {"label": "24", "value": 24},
                                                                                                {"label": "25", "value": 25},
                                                                                                {"label": "26", "value": 26},
                                                                                                {"label": "27", "value": 27}])
                except:
                    logger.warning('Unable to update database')

        if self.hx711_update == None or self.hx711_update != self.version:
            try:
                 await self.cbpi.config.add(self.name+"_update", self.version,type=ConfigType.STRING, description='HX711 Version update', source='hidden')
            except Exception as e:
                logger.warning('Unable to update database')
                logger.warning(e)


@parameters([Property.Select(label="dout", options=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27], description="GPIO Pin connected to the Serial Data Output Pin of the HX711"),
    Property.Select(label="pd_sck", options=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27], description="GPIO Pin connected to the Power Down & Seerial Clock Pin of the HX711"),
    #Property.Select(label="gain", options = [128,64, 32],description = "Select gain for HX711"),
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
        self.offset = int(float(self.props.get("offset",0)))
        self.scale = int(float(self.props.get("scale",1)))
        self.calibration_active = False
        self.measurement_is_running = False


        logging.info("INIT HX711:")
        logging.info("dout: {}".format(self.dout))
        logging.info("pd_sck: {}".format(self.pd_sck))
        logging.info("gain: {}".format(self.gain))
        logging.info("offset: {}".format(self.offset))
        logging.info("scale: {}".format(self.scale))

        logging.info("Setup HX711")
        global hx

    @action(key="Tare Sensor", parameters=[])
    async def Reset(self, **kwargs):
        hx.zero()
        logging.info("Tare HX711 Loadcell")

    def tarereset(self):
        hx.zero()
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
        hx.zero()
        logging.info("Reset")
        self.zeroValue=hx.read(Options(10))
        logging.info("Calibrate HX711 Loadcell")
        self.cbpi.notify("Loadcell Calibration", "Please put your known weight on the scale and press next", NotificationType.INFO, action=[NotificationAction("Next Step", self.NextStep)])
        while not self.next == True:
            await asyncio.sleep(1)
            pass
        self.next = False

        self.raw = hx.read(Options(10))
        self.refUnitFloat = round(((self.raw-self.zeroValue) / self.weight),2)
        self.refUnit = round(self.refUnitFloat, 0)
        if self.refUnit == 0:
            self.refUnit=1

        #logging.info("Scale Factor {}".format(self.calibration_factor))
        self.cbpi.notify("Loadcell Calibration done", "Enter these values in the sensor hardware. Offset: {}; Scale: {}".format(self.zeroValue, self.refUnit),action=[NotificationAction("Next Step", self.NextStep)])
        while not self.next == True:
            await asyncio.sleep(1)
            pass
        self.next = False
        hx.setReferenceUnit(self.refUnit)
        hx.setOffset(self.zeroValue)
        logging.info("Tare")
        hx.zero()
        self.calibration_active = False

    async def NextStep(self):
        self.next = True
        pass

    async def run(self):
        ready= False
        while ready is False:
            try:
                hx.setUnit(Mass.Unit.G)
                hx.setReferenceUnit(self.scale)
                hx.setOffset(self.offset)
                logging.info("Tare")
                hx.zero()
                ready=True
            except:
                pass




        while self.running is True:
            try:
                if self.calibration_active == False:
                    self.measurement_is_running = True
                    self.value = round(float(hx.weight(5)),2)
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
             Property.Select(label="Reset", options=["Yes","No"],description="Tare Weight before starting")])


class WeightStep(CBPiStep):

    async def on_timer_done(self,timer):
        self.summary = ""
        self.cbpi.notify(self.name, 'Step finished. Transferred {} {}.'.format(round(self.current_volume,2),'L'), NotificationType.SUCCESS)

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

        self.preresetsensor = self.props.get("Reset","Yes")
        self.dens_flag = True if self.props.get("useDensity", "No") == "Yes" else False
        self.density = float(self.props.get("Density",0))
        if self.preresetsensor == "Yes":
            self.sensor.instance.tarereset()

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
            self.summary="Volume: {}, Target: {}".format(self.current_volume , self.target_volume)
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
