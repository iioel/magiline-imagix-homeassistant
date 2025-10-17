"""The Pool Monitor integration."""
from __future__ import annotations

import asyncio
import logging
from datetime import timedelta
from typing import Any

import aiohttp
import async_timeout

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

_LOGGER = logging.getLogger(__name__)

DOMAIN = "magiline_imagix"
PLATFORMS: list[Platform] = [Platform.SENSOR]
SCAN_INTERVAL = timedelta(seconds=30)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Pool Monitor from a config entry."""
    coordinator = PoolDataUpdateCoordinator(hass, entry)
    
    # Fetch initial data
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Setup platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


class PoolDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Pool data from the API."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize."""
        self.host = entry.data["host"]
        self.path = entry.data.get("path", "/api/v1/pool/info")
        self.session = async_get_clientsession(hass)
        
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{entry.entry_id}",
            update_interval=SCAN_INTERVAL,
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from API."""
        url = f"http://{self.host}{self.path}"
        
        try:
            async with async_timeout.timeout(10):
                async with self.session.get(url) as response:
                    if response.status != 200:
                        # Use debug level to avoid log spam
                        _LOGGER.debug(
                            "Error fetching pool data from %s: HTTP %s", 
                            url, 
                            response.status
                        )
                        raise UpdateFailed(f"HTTP error {response.status}")
                    
                    data = await response.json()
                    _LOGGER.debug("Successfully fetched pool data")
                    return data
                    
        except aiohttp.ClientError as err:
            _LOGGER.debug("Connection error fetching pool data from %s: %s", url, err)
            raise UpdateFailed(f"Connection error: {err}") from err
        except asyncio.TimeoutError as err:
            _LOGGER.debug("Timeout fetching pool data from %s", url)
            raise UpdateFailed("Timeout connecting to pool") from err
        except Exception as err:
            _LOGGER.debug("Unexpected error fetching pool data from %s: %s", url, err)
            raise UpdateFailed(f"Unexpected error: {err}") from err
