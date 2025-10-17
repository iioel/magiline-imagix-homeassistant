"""Support for Pool Monitor sensors."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import DOMAIN, SENSOR_DEFINITIONS

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Pool Monitor sensors from a config entry."""
    coordinator: DataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    
    sensors = []
    
    # Create sensors based on definitions
    for sensor_def in SENSOR_DEFINITIONS:
        sensors.append(
            PoolSensor(
                coordinator=coordinator,
                entry=entry,
                sensor_def=sensor_def,
            )
        )
    
    async_add_entities(sensors)


class PoolSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Pool Monitor sensor."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        entry: ConfigEntry,
        sensor_def: dict,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        
        self._sensor_def = sensor_def
        self._attr_unique_id = f"{entry.entry_id}_{sensor_def['key']}"
        self._attr_translation_key = sensor_def["key"]
        self._entry = entry
        
        # Set name
        self._attr_name = sensor_def["name"]
        
        # Set icon
        if "icon" in sensor_def:
            self._attr_icon = sensor_def["icon"]
        
        # Set device class if specified
        if "device_class" in sensor_def:
            self._attr_device_class = sensor_def["device_class"]
        
        # Set state class if specified
        if "state_class" in sensor_def:
            self._attr_state_class = sensor_def["state_class"]
        
        # Set unit of measurement if specified
        if "unit" in sensor_def:
            self._attr_native_unit_of_measurement = sensor_def["unit"]
        
        # Set device info for grouping
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Pool Monitor",
            manufacturer="Pool Controller",
            model="API Integration",
        )

    @property
    def native_value(self) -> Any:
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None
        
        # Navigate through the data path
        value = self.coordinator.data
        path = self._sensor_def["path"]
        
        try:
            for key in path:
                if isinstance(key, int):
                    # Array index
                    if isinstance(value, list) and len(value) > key:
                        value = value[key]
                    else:
                        return None
                else:
                    # Dictionary key
                    if isinstance(value, dict) and key in value:
                        value = value[key]
                    else:
                        return None
            
            return value
            
        except (KeyError, IndexError, TypeError) as err:
            _LOGGER.debug(
                "Error getting value for %s: %s", self._attr_name, err
            )
            return None

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        # Sensor is available if we have data, even if update failed
        return self.coordinator.data is not None

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return additional attributes if specified."""
        if "attributes" not in self._sensor_def:
            return None
        
        if not self.coordinator.data:
            return None
        
        attrs = {}
        for attr_key, attr_path in self._sensor_def["attributes"].items():
            value = self.coordinator.data
            try:
                for key in attr_path:
                    if isinstance(key, int):
                        if isinstance(value, list) and len(value) > key:
                            value = value[key]
                        else:
                            break
                    else:
                        if isinstance(value, dict) and key in value:
                            value = value[key]
                        else:
                            break
                else:
                    # Only add attribute if we successfully navigated the path
                    attrs[attr_key] = value
            except (KeyError, IndexError, TypeError):
                pass
        
        return attrs if attrs else None
