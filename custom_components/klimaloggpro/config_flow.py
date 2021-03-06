"""Config flow for klimaloggpro integration."""
import logging

import voluptuous as vol

from homeassistant import config_entries, core, exceptions

from .const import DOMAIN  # pylint:disable=unused-import

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("name", default="Klimalogg"): str, 
        vol.Optional("sensor_0temp", default=True): bool, 
        vol.Optional("sensor_0humid", default=True): bool, 
        vol.Optional("sensor_1temp"): bool, 
        vol.Optional("sensor_1humid"): bool, 
        vol.Optional("sensor_2temp"): bool,
        vol.Optional("sensor_2humid"): bool,
        vol.Optional("sensor_3temp"): bool,
        vol.Optional("sensor_3humid"): bool,
        vol.Optional("sensor_4temp"): bool,
        vol.Optional("sensor_4humid"): bool,
        vol.Optional("sensor_5temp"): bool,
        vol.Optional("sensor_5humid"): bool,
        vol.Optional("sensor_6temp"): bool,
        vol.Optional("sensor_6humid"): bool,
        vol.Optional("sensor_7temp"): bool,
        vol.Optional("sensor_7humid"): bool,
        vol.Optional("sensor_8temp"): bool,
        vol.Optional("sensor_8humid"): bool,
    }
)

async def validate_input(hass: core.HomeAssistant, data: dict):
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    # TODO validate the data can be used to set up a connection.

    # If your PyPI package is not built with async, pass your methods
    # to the executor:
    # await hass.async_add_executor_job(
    #     your_validate_func, data["username"], data["password"]
    # )

    # hub = PlaceholderHub(data["host"])

    #if not await hub.authenticate(data["username"], data["password"]):
    #    raise InvalidAuth
    if len(data["name"]) < 3:
        raise CannotConnect
    # If you cannot connect:
    # throw CannotConnect
    # If the authentication is wrong:
    # InvalidAuth

    # Return info that you want to store in the config entry.
    return {"title": data["name"]}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for klimaloggpro."""

    VERSION = 1
    # Not sure about connection class - Driver reads values from device like every 10 seconds
    # Does it makes sense, to make it local push, so the read values get pushed to HA?
    # Local poll works just fine for the moment.
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)

                return self.async_create_entry(title=info["title"], data=user_input)
            # TODO Add some real-world Exceptions...?
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(exceptions.HomeAssistantError):
    """Error to indicate there is invalid auth."""
