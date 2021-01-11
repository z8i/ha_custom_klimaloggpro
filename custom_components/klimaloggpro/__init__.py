"""The klimaloggpro integration."""
import asyncio
import logging
import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

#import kloggpro.klimalogg

_LOGGER = logging.getLogger(__name__)
_LOGGER.info("Init wird geladen")

CONFIG_SCHEMA = vol.Schema({DOMAIN: vol.Schema({})}, extra=vol.ALLOW_EXTRA)

# TODO List the platforms that you want to support.
# For your initial PR, limit it to 1 platform.
PLATFORMS = ["sensor"]


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the klimaloggpro component."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up klimaloggpro from a config entry."""
    # TODO Store an API object for your platforms to access
    
    _LOGGER.info("kurz vorm treiber-laden")

    #hass.data[DOMAIN][entry.entry_id] = kloggpro.klimalogg.KlimaLoggDriver()
    #hass.data[DOMAIN]["horst"] = kloggpro.klimalogg.KlimaLoggDriver()

    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in PLATFORMS
            ]
        )
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
