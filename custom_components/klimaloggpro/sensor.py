"""Platform for sensor integration."""

import random
import logging

from homeassistant.const import (
    DEVICE_CLASS_TEMPERATURE,
    TEMP_CELSIUS,
    ATTR_TEMPERATURE,
    DEVICE_CLASS_HUMIDITY,
    PERCENTAGE,
    STATE_UNKNOWN
)
from homeassistant.helpers.entity import Entity
from .const import DOMAIN


_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_devices):
    """Add sensors for passed config_entry in HA."""
    data = hass.data[DOMAIN][config_entry.entry_id]
    kldr = hass.data[DOMAIN]["kldr"]
    sensorlist_temp=[]
    sensorlist_humid=[]
    for sensor in range(9):
        if data.get(f"sensor_{sensor}temp", False):
            sensorlist_temp.append(f"{sensor}")
        if data.get(f"sensor_{sensor}humid", False):
            sensorlist_humid.append(f"{sensor}")

    _LOGGER.info(f"Temp. sensor {sensorlist_temp} and Humid. sensor {sensorlist_humid} to configure")
    new_devices = []
    for sensor in sensorlist_temp:
        new_devices.append(TemperatureSensor(kldr, sensor))
    for sensor in sensorlist_humid:
        new_devices.append(HumiditySensor(kldr, sensor))
    if new_devices:
        async_add_devices(new_devices)

class SensorBase(Entity):
    """ Base representation of KlimaLoggPro Sensors """
    should_poll = True

    def __init__(self, kldr, sensor):
        """ Initialize sensor """
        self._kldr = kldr
        self._sensornum = sensor
    
    @property
    def device_info(self):
        """Return information to link this entity with the correct device."""
        return {"identifiers": {(DOMAIN, self._kldr.get_transceiver_id())}}

    @property
    def available(self) -> bool:
        """Return True if roller and hub is available."""
        return self._kldr.transceiver_is_present()


class TemperatureSensor(SensorBase):
    """ Temperatursensor """
    device_class = DEVICE_CLASS_TEMPERATURE

    @property
    def unique_id(self):
        """Return Unique ID string."""
        return f"{self._kldr.get_transceiver_id()}_temp{self._sensornum}"

    @property
    def device_state_attributes(self):
        """Return the state attributes of the device."""
        attr = {}
        attr["max_temp"] = f"{self._kldr._service.current.values[f'Temp{self._sensornum}Max']:.1f}"
        attr["signal_strength"] = self._kldr._service.current.values['SignalQuality']
        return attr

    @property
    def state(self):
        """Return the state of the sensor."""
        value = self._kldr._service.current.values[f"Temp{self._sensornum}"]
        if value == 81.1: # if no value was read, the stored value by the driver is 81.1, some offset...
            return STATE_UNKNOWN
            
        # had some trouble with floats being 20.0000009, that fixed it somehow
        # by returning a string, it is not displayed in HA UI, but maybe not good code either...
        return f"{value:.1f}"

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    @property
    def name(self):
        """Return the name of the sensor."""
        if not(self._sensornum == "0"): # Sensor 0 has no name in the driver - it's the sensor in the station itself
            sensorname = self._kldr._service.station_config.values[f"SensorText{self._sensornum}"]
            sensorname = sensorname.capitalize()
        else:
            sensorname = "Indoor"
        return f"{sensorname} Temperature {self._sensornum}"



class HumiditySensor(SensorBase):
    """ Humiditysensor """
    device_class = DEVICE_CLASS_HUMIDITY

    @property
    def unique_id(self):
        """Return Unique ID string."""
        return f"{self._kldr.get_transceiver_id()}_humidity{self._sensornum}"

    @property
    def device_state_attributes(self):
        """Return the state attributes of the device."""
        attr = {}
        attr["max_humidity"] = f"{self._kldr._service.current.values[f'Humidity{self._sensornum}Max']:.1f}"
        attr["signal_strength"] = self._kldr._service.current.values['SignalQuality']
        return attr

    @property
    def state(self):
        """Return the state of the sensor."""
        value = self._kldr._service.current.values[f"Humidity{self._sensornum}"]
        if value == 110.0: # if no value was read, the stored value by the driver is 110.0, some offset...
            return STATE_UNKNOWN
        return f"{value:.0f}"

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return PERCENTAGE

    @property
    def name(self):
        """Return the name of the sensor."""
        if not(self._sensornum == "0"): # Sensor 0 has no name in the driver - it's the sensor in the station itself
            sensorname = self._kldr._service.station_config.values[f"SensorText{self._sensornum}"]
            sensorname = sensorname.capitalize()
        else:
            sensorname = "Indoor"
        return f"{sensorname} Humidity {self._sensornum}"