# Pool Monitor Integration for Home Assistant

This custom integration fetches data from a pool monitoring API and displays it in Home Assistant.

## Installation

1. Copy the `pool_monitor` directory to your `custom_components` directory in your Home Assistant config folder
2. Restart Home Assistant
3. Go to Configuration → Integrations
4. Click "+ Add Integration"
5. Search for "Pool Monitor"
6. Enter your pool's IP address and optionally customize the API path

## Features

- UI-based configuration
- Automatic sensor type detection
- Graceful error handling (no log spam if pool is offline)
- Auto-discovery of all data points from the API
- Proper device grouping in Home Assistant