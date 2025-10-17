"""Config flow for Pool Monitor integration."""
from __future__ import annotations

import asyncio
import logging
from typing import Any

import aiohttp
import async_timeout
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

DOMAIN = "magiline_imagix"
CONF_PATH = "path"
DEFAULT_PATH = "/api/v1/pool/info"

_LOGGER = logging.getLogger(__name__)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""
    host = data[CONF_HOST]
    path = data.get(CONF_PATH, DEFAULT_PATH)
    url = f"http://{host}{path}"
    
    session = async_get_clientsession(hass)
    
    try:
        async with async_timeout.timeout(10):
            async with session.get(url) as response:
                if response.status != 200:
                    raise CannotConnect(f"HTTP {response.status}")
                
                # Try to parse as JSON to validate it's a valid API
                await response.json()
                
    except aiohttp.ClientError as err:
        raise CannotConnect(f"Connection failed: {err}") from err
    except asyncio.TimeoutError as err:
        raise CannotConnect("Connection timeout") from err
    except Exception as err:
        raise CannotConnect(f"Unknown error: {err}") from err
    
    return {"title": f"Pool Monitor ({host})"}


class PoolMonitorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Pool Monitor."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                # Create unique ID based on host
                await self.async_set_unique_id(user_input[CONF_HOST])
                self._abort_if_unique_id_configured()
                
                return self.async_create_entry(title=info["title"], data=user_input)

        data_schema = vol.Schema(
            {
                vol.Required(CONF_HOST, default="192.168.1.52:11000"): str,
                vol.Optional(CONF_PATH, default=DEFAULT_PATH): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )


class CannotConnect(Exception):
    """Error to indicate we cannot connect."""
