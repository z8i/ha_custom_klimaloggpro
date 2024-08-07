"""The klimaloggpro integration."""
import asyncio
import logging
import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import (
    EVENT_HOMEASSISTANT_STOP
)

from .const import DOMAIN

import kloggpro.klimalogg

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema({DOMAIN: vol.Schema({})}, extra=vol.ALLOW_EXTRA)

PLATFORMS = ["sensor"] #KlimaLogg provides some temperature and humidity sensors

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the klimaloggpro component."""
    hass.data.setdefault(DOMAIN, {}) 
                    # Needed to create the entry for this component inside the hass object, 
                    # without it, it is not possible to store data across this integration?
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up klimaloggpro from a config entry."""
    hass.data[DOMAIN][entry.entry_id] = entry.data # not sure, if this is needed...
    
    loop = asyncio.get_event_loop()
    kldr = await loop.run_in_executor(None, kloggpro.klimalogg.KlimaLoggDriver)

    hass.data[DOMAIN]["kldr"] = kldr
    await loop.run_in_executor(None, kldr.clear_wait_at_start) # necessary from the klimalogg-driver
    _LOGGER.info("Driver set up and started, push 'USB' Button on Logger now!")

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    def shutdown(event):
        _LOGGER.info("Just before shutdown, KlimaLoggDriver will get shut down.")
        hass.data[DOMAIN]["kldr"].shutDown() # releases the USB interface!
    
    # saw this below in the devolo_home_control integration - is it reasonable to store the listener?
    #hass.data[DOMAIN][entry.entry_id]["listener"] = hass.bus.async_listen_once(
    hass.bus.async_listen_once(
        EVENT_HOMEASSISTANT_STOP, shutdown
    )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    hass.data[DOMAIN]["kldr"].shutDown()
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in PLATFORMS
            ]
        ),    
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
