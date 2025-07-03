# House Temperature Tracker

A Python Flask web application for monitoring Nest thermostat data and house temperatures over time.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up Nest API access:

   **Step 1: Create a Device Access Project**
   - Go to https://console.nest.google.com/device-access
   - Click "Create project"
   - Enter a project name (e.g., "House Temperature Tracker")
   - Accept the terms and conditions
   - Pay the one-time $5 fee (required by Google)
   - Save your **Project ID** (format: `enterprise/project-id`)

   **Step 2: Enable Smart Device Management API**
   - Go to https://console.cloud.google.com
   - Create a new project or select an existing one
   - Go to "APIs & Services" > "Enable APIs and Services"
   - Search for "Smart Device Management API"
   - Click on it and press "Enable"

   **Step 3: Create OAuth 2.0 Credentials**
   - In Google Cloud Console, go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - If prompted, configure the OAuth consent screen first:
     - Choose "External" user type
     - Fill in required fields (app name, email)
     - Add your email to test users
   - For Application type, choose "Web application"
   - Add authorized redirect URI: `https://www.google.com/`
   - Save and copy your **Client ID** and **Client Secret**

   **Step 4: Link Your Nest Account**
   - Go to: `https://nestservices.google.com/partnerconnections/[YOUR_PROJECT_ID]/auth?redirect_uri=https://www.google.com&access_type=offline&prompt=consent&client_id=[YOUR_CLIENT_ID]&response_type=code&scope=https://www.googleapis.com/auth/sdm.service`
   - Replace `[YOUR_PROJECT_ID]` with your Device Access project ID
   - Replace `[YOUR_CLIENT_ID]` with your OAuth client ID
   - Sign in with your Google account that has Nest devices
   - Allow permissions
   - You'll be redirected to Google with a code in the URL

   **Step 5: Get Refresh Token**
   - Copy the authorization code from the redirect URL (after `code=`)
   - Use curl or Postman to exchange it for tokens:
   ```bash
   curl -X POST "https://www.googleapis.com/oauth2/v4/token" \
     -d "client_id=[YOUR_CLIENT_ID]" \
     -d "client_secret=[YOUR_CLIENT_SECRET]" \
     -d "code=[AUTHORIZATION_CODE]" \
     -d "grant_type=authorization_code" \
     -d "redirect_uri=https://www.google.com"
   ```
   - Save the **refresh_token** from the response

3. Configure environment:
   - Copy `.env.example` to `.env`
   - Fill in your credentials:
     - `NEST_CLIENT_ID`: From Step 3
     - `NEST_CLIENT_SECRET`: From Step 3
     - `NEST_PROJECT_ID`: From Step 1 (include the "enterprise/" prefix)
     - `NEST_REFRESH_TOKEN`: From Step 5
     - `FLASK_SECRET_KEY`: Generate a random string for session security

4. Set up data collection with cron:
   - Find your Python path: `which python3`
   - Edit your crontab: `crontab -e`
   - Add this line for data collection every minute:
   ```
   */1 * * * * /usr/bin/python3 /path/to/your/house-temp-tracker/collect_data.py
   ```
   - Replace `/usr/bin/python3` with your actual Python path
   - Replace `/path/to/your/house-temp-tracker/` with your actual project path
   - You can adjust the interval (e.g., `*/5` for every 5 minutes)

5. Run the application:
```bash
python run.py
```

6. Access the web interface at http://localhost:5000

## Features

- Real-time temperature and humidity monitoring
- Historical data visualization with interactive charts
- Temperature statistics (average, min, max)
- HVAC status tracking
- Automatic data collection via cron job
- Responsive web interface

## Architecture

- **Backend**: Python Flask
- **Database**: SQLite
- **Frontend**: HTML/CSS with minimal JavaScript for charts
- **Data Collection**: Cron job for periodic Nest API polling

## Troubleshooting

**No devices found:**
- Ensure your Google account has Nest devices linked
- Verify all API credentials are correct
- Check that the Smart Device Management API is enabled
- Make sure your OAuth consent screen includes your email as a test user

**Authentication errors:**
- Refresh tokens don't expire, but access tokens do (handled automatically)
- If you get 401 errors, try generating a new refresh token
- Ensure your Project ID includes the "enterprise/" prefix

**Missing temperature data:**
- Check that your cron job is running properly: `crontab -l`
- Verify the Python path and project path in your cron job are correct
- Check system logs for cron execution: `grep CRON /var/log/syslog` (Linux) or `log show --predicate 'process == "cron"' --last 1h` (macOS)
- Test manual data collection: `python collect_data.py`
- Verify your Nest device supports temperature reporting