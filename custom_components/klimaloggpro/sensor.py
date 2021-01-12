"""Platform for sensor integration."""
# This file shows the setup for the sensors associated with the cover.
# They are setup in the same way with the call to the async_setup_entry function
# via HA from the module __init__. Each sensor has a device_class, this tells HA how
# to display it in the UI (for know types). The unit_of_measurement property tells HA
# what the unit is, so it can display the correct range. For predefined types (such as
# battery), the unit_of_measurement should match what's expected.
import random

from homeassistant.const import (
    DEVICE_CLASS_TEMPERATURE,
    TEMP_CELSIUS,
    ATTR_TEMPERATURE,
    STATE_UNKNOWN
)
from homeassistant.helpers.entity import Entity
from .const import DOMAIN

import kloggpro.klimalogg

async def async_setup_entry(hass, config_entry, async_add_devices):
    """Add sensors for passed config_entry in HA."""
    #kldr = hass.data[DOMAIN][config_entry.entry_id]
    kldr = kloggpro.klimalogg.KlimaLoggDriver()
    kldr.clear_wait_at_start()
    sensorlist = ["0", "1", "3"]
    new_devices = []
    for sensor in sensorlist:
        new_devices.append(TemperatureSensor(kldr, sensor))
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
        if value == 81.1:
            return STATE_UNKNOWN
        return f"{value:.1f}"

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    @property
    def name(self):
        """Return the name of the sensor."""
        if not(self._sensornum == "0"):
            sensorname = self._kldr._service.station_config.values[f"SensorText{self._sensornum}"]
        else:
            sensorname = "Indoor"
        return f"{sensorname} Klimlogg Sensor {self._sensornum}"