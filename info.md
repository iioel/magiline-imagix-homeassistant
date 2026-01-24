# Magiline iMAGI-X Pool Integration

This integration allows you to monitor your Magiline iMAGI-X pool system directly in Home Assistant.

## Features

- 🏊 Real-time pool monitoring
- 📊 Automatic sensor creation from API data
- 🔄 Configurable polling interval (5-300 seconds)
- 🎛️ UI-based configuration flow
- 📱 Device grouping in Home Assistant
- 🔕 Graceful error handling (no log spam when pool is offline)
- 🌐 Local polling (no cloud required)

## Configuration

The integration can be configured through the Home Assistant UI:

1. Go to **Settings** → **Devices & Services** → **Integrations**
2. Click **"+ Add Integration"**
3. Search for **"Magiline iMAGI-X"**
4. Enter your pool's IP address (e.g., `192.168.1.52:11000`)
5. Optionally customize the API path (default: `/api/v1/pool/info`)
6. Configure the scan interval in the integration options

## Requirements

- Magiline iMAGI-X pool controller accessible on your local network
- Home Assistant 2025.10.2 or later

## Support

For issues and feature requests, please visit the [GitHub repository](https://github.com/iioel/magiline-imagix-homeassistant/issues).
