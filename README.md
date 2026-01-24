# Magiline iMAGI-X Integration for Home Assistant

This custom integration fetches data from a pool monitoring API and displays it in Home Assistant.

## Installation

### Installation via HACS (Recommended)

1. Ensure [HACS](https://hacs.xyz/) is installed in your Home Assistant instance
2. In Home Assistant, go to HACS → Integrations
3. Click the three dots menu in the top right corner
4. Select "Custom repositories"
5. Add the repository URL: `https://github.com/iioel/magiline-imagix-homeassistant`
6. Select category: "Integration"
7. Click "Add"
8. Find "Magiline iMAGI-X" in the HACS integrations list and click "Download"
9. Restart Home Assistant
10. Go to Settings → Devices & Services → Integrations
11. Click "+ Add Integration"
12. Search for "Magiline iMAGI-X" or "Pool Monitor"
13. Enter your pool's IP address and optionally customize the API path

### Manual Installation

1. Copy the `magiline-imagix` directory to your `custom_components` directory in your Home Assistant config folder
2. Restart Home Assistant
3. Go to Configuration → Integrations
4. Click "+ Add Integration"
5. Search for "Pool Monitor"
6. Enter your pool's IP address and optionally customize the API path

## Features

- UI-based configuration
- Graceful error handling (no log spam if pool is offline)
- Proper device grouping in Home Assistant