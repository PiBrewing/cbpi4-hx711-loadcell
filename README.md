# Craftbeerpi4 Plugin for HX711 loadcell 

Loadcell must be hooked up to a HX711 controller to readout the data 

## Software installation:

This plugin requires additional packages for the installation that MUST be installed / complied BEFORE you install the plugin!!!

Please install the required development packages:

`sudo apt-get install -y liblgpio-dev`

Then, you need to clone the hx711 repository as it serves as basis for the python package:

`git clone --depth=1 https://github.com/endail/hx711`

Now change to the package directory and compile the package:

`cd hx711`
`make && make install`

Then run `sudo ldconfig` to allow other packages to access the hx711 library.

Afterwards, you can install the hx711 python package first or move directly to the installation of the hx711 loadcell plugin:

`pipx runpip cbpi4 install hx711-rpi-py`

For the installation of the plugin, please have a look at the [Craftbeerpi4 Documentation](https://openbrewing.gitbook.io/craftbeerpi4_support/readme/plugin-installation)

- Package name: cbpi4-hx711-loadcell (not yet available)
- Package link: https://github.com/PiBrewing/cbpi4-hx711-loadcell/archive/main.zip (not yet under main available)

Development link: https://github.com/PiBrewing/cbpi4-hx711-loadcell/archive/development.zip


## Hardware Installation:

To be added 


## Sensor Configuration

From 0.0.4 to 0.1.0 some major changes had to be made. The sensor GPIO configuration must be done in the global settings and not on the sensor hardware page itself. Currently, only 1 sensor can be used.

Calibration is done on the sensor hardware section.

More information to be added.


### Changelog:

- 14.08.24: (0.1.0) Conversion to new hx711 library which is required for bookworm in combination with lgpio
- XX.XX.XX: (0.0.4) Old Version