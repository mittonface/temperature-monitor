# Weather API Setup Guide

This application now supports displaying outside temperature data alongside your indoor temperature readings. The weather data is fetched from OpenWeatherMap API.

## Configuration Steps

1. **Get an OpenWeatherMap API Key**

   - Sign up for a free account at https://openweathermap.org/api
   - Navigate to your API keys section
   - Copy your API key

2. **Find Your Location Coordinates**

   - Visit https://www.latlong.net/ or use Google Maps
   - Find your location and get the latitude and longitude
   - You'll need these for accurate weather data

3. **Update the .env File**
   Add these lines to your `.env` file:
   ```
   # Weather API Configuration (OpenWeatherMap)
   OPENWEATHER_API_KEY=your_api_key_here
   LOCATION_LAT=your_latitude
   LOCATION_LON=your_longitude
   ```
4. **Run Database Migration**
   The application needs to update the database to store outside temperature data:
   ```bash
   python migrations/add_outside_temperature.py
   ```

## Features Added

- **Outside Temperature on Graph**: A purple dashed line shows the outside temperature alongside your indoor readings
- **Current Outside Temperature**: Displayed in the main stats cards
- **Outside Temperature Statistics**: Min, max, and average outside temperature in the statistics section

## Troubleshooting

- If you see "--°C" for outside temperature, check that your API key and coordinates are properly configured
- The weather data is fetched whenever temperature data is collected from your Nest devices
- Weather API has rate limits on the free tier (1000 calls/day), which should be sufficient for typical usage
