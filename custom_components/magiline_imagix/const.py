"""Constants for the Pool Monitor integration."""

from homeassistant.const import (
    UnitOfTemperature,
    UnitOfPower,
    UnitOfEnergy,
    PERCENTAGE,
)

DOMAIN = "magiline_imagix"

CONF_PATH = "path"
DEFAULT_PATH = "/api/v1/pool/info"

# Comprehensive sensor definitions
SENSOR_DEFINITIONS = [
    # Pump Sensors (from state.cards.pumps[0])
    {
        "key": "pump_state",
        "name": "Pump State",
        "path": ["state", "cards", "pumps", 0, "state"],
        "icon": "mdi:pump",
    },
    {
        "key": "pump_rpm",
        "name": "Pump Speed",
        "path": ["state", "cards", "pumps", 0, "rpm"],
        "icon": "mdi:pump",
        "unit": "RPM",
        "state_class": "measurement",
    },
    {
        "key": "pump_power",
        "name": "Pump Power",
        "path": ["state", "cards", "pumps", 0, "power"],
        "device_class": "power",
        "unit": UnitOfPower.WATT,
        "state_class": "measurement",
    },
    {
        "key": "pump_power_total",
        "name": "Pump Total Energy",
        "path": ["state", "cards", "pumps", 0, "powerTotal"],
        "device_class": "energy",
        "unit": UnitOfEnergy.WATT_HOUR,
        "state_class": "total_increasing",
    },
    {
        "key": "pump_slab_close",
        "name": "Pump Slab Closed",
        "path": ["state", "cards", "pumps", 0, "slabClose"],
        "icon": "mdi:valve",
    },
    {
        "key": "pump_water_present",
        "name": "Pump Water Present",
        "path": ["state", "cards", "pumps", 0, "waterPresent"],
        "icon": "mdi:water-check",
    },
    
    # Electrolyzer Sensors (from state.cards.electrolyzer)
    {
        "key": "electrolyzer_state",
        "name": "Electrolyzer State",
        "path": ["state", "cards", "electrolyzer", "state"],
        "icon": "mdi:water-plus",
    },
    
    # Spotlight Sensors (from state.spotlight)
    {
        "key": "spotlight_state",
        "name": "Spotlight State",
        "path": ["state", "spotlight", "state"],
        "icon": "mdi:spotlight",
    },
    {
        "key": "spotlight_mode",
        "name": "Spotlight Mode",
        "path": ["state", "spotlight", "mode"],
        "icon": "mdi:spotlight",
    },
    
    # Roller Sensors (from state.roller)
    {
        "key": "roller_state",
        "name": "Pool Cover State",
        "path": ["state", "roller", "state"],
        "icon": "mdi:window-shutter",
    },
    {
        "key": "roller_mode",
        "name": "Pool Cover Mode",
        "path": ["state", "roller", "mode"],
        "icon": "mdi:window-shutter",
    },
    {
        "key": "roller_position",
        "name": "Pool Cover Position",
        "path": ["state", "roller", "position"],
        "icon": "mdi:window-shutter",
    },
    
    # Remote Sensors (from state.remote)
    {
        "key": "remote_number",
        "name": "Remote Number",
        "path": ["state", "remote", "number"],
        "icon": "mdi:remote",
    },
    {
        "key": "remote_state",
        "name": "Remote State",
        "path": ["state", "remote", "state"],
        "icon": "mdi:remote",
    },
    
    # Filtration Sensors (from state.filtration)
    {
        "key": "filtration_mode",
        "name": "Filtration Mode",
        "path": ["state", "filtration", "mode"],
        "icon": "mdi:filter",
    },
    {
        "key": "filtration_actual_prog",
        "name": "Filtration Program",
        "path": ["state", "filtration", "actualProg"],
        "icon": "mdi:filter-settings",
    },
    {
        "key": "filtration_state",
        "name": "Filtration State",
        "path": ["state", "filtration", "state"],
        "icon": "mdi:filter",
    },
    {
        "key": "filtration_swimming_remain",
        "name": "Swimming Mode Remaining Time",
        "path": ["state", "filtration", "swimming", "remainTime"],
        "icon": "mdi:timer-sand",
        "unit": "min",
        "state_class": "measurement",
    },
    {
        "key": "filtration_pause_remain",
        "name": "Pause Remaining Time",
        "path": ["state", "filtration", "pause", "remainTime"],
        "icon": "mdi:timer-pause",
        "unit": "min",
        "state_class": "measurement",
    },
    
    # Water Quality Metrics (from state.metrics)
    {
        "key": "water_temperature",
        "name": "Water Temperature",
        "path": ["state", "metrics", "waterTemperature"],
        "device_class": "temperature",
        "unit": UnitOfTemperature.CELSIUS,
        "state_class": "measurement",
    },
    {
        "key": "air_temperature",
        "name": "Air Temperature",
        "path": ["state", "metrics", "airTemperature"],
        "device_class": "temperature",
        "unit": UnitOfTemperature.CELSIUS,
        "state_class": "measurement",
    },
    {
        "key": "ph",
        "name": "pH Level",
        "path": ["state", "metrics", "ph"],
        "icon": "mdi:ph",
        "state_class": "measurement",
        "attributes": {
            "alarm_min": ["state", "metrics", "phAlarmLimits", 0],
            "alarm_max": ["state", "metrics", "phAlarmLimits", 1],
        },
    },
    {
        "key": "orp",
        "name": "ORP (Redox)",
        "path": ["state", "metrics", "orp"],
        "icon": "mdi:water-check",
        "unit": "mV",
        "state_class": "measurement",
        "attributes": {
            "alarm_min": ["state", "metrics", "orpAlarmLimits", 0],
            "alarm_max": ["state", "metrics", "orpAlarmLimits", 1],
        },
    },
    {
        "key": "free_chlorine",
        "name": "Free Chlorine",
        "path": ["state", "metrics", "freeChlorine"],
        "icon": "mdi:flask",
        "unit": "mg/L",
        "state_class": "measurement",
    },
    {
        "key": "salinity",
        "name": "Salinity",
        "path": ["state", "metrics", "salinity"],
        "icon": "mdi:shaker",
        "unit": "g/L",
        "state_class": "measurement",
        "attributes": {
            "alarm_min": ["state", "metrics", "salinityAlarmLimits", 0],
        },
    },
    {
        "key": "water_hardness",
        "name": "Water Hardness",
        "path": ["state", "metrics", "waterHardness"],
        "icon": "mdi:water-opacity",
        "unit": "°f",
        "state_class": "measurement",
    },
    {
        "key": "filter_clogging",
        "name": "Filter Clogging",
        "path": ["state", "metrics", "filterClogging"],
        "icon": "mdi:air-filter",
        "unit": PERCENTAGE,
        "state_class": "measurement",
    },
]
