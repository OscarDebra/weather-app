# Installation and setup

1. Run `git clone https://github.com/OscarDebra/weather-app.git` to clone the project on your device.
2. Run `docker compose up --build` while in the weather-app folder to build the project on the device.
3. To verify it's working visit the backend container on the device where the container is hosted by searching `http://localhost`.
4. To open the container on another device, find the ip of the device where the container is hosted, then visit `http://http://Oscars-MacBook-Pro.local`

# User guide

This project currenty has a frontend and backend container with 3 endpoints.

1. To verify if the app is working on your device, first make sure you are on the same network, then visit `http://Oscars-MacBook-Pro.local`, where the ip is the ip of the device where the container is hosted, this is the frontend.
2. The second endpoint is located at `http://Oscars-MacBook-Pro.local/api/weather` and currently returns the projected temperature each hour for the next week at a very specific location.
3. The third endpoint is at `http://Oscars-MacBook-Pro.local/api/health` and returns if the api is working.

# About the project

This project consists of three docker containers. One frontend container in react, a backend container using fastapi and a caddy container.

The physical architecture consists of a raspberry pi, but is currently hosted on a macbook while under development, but the raspi can be substituted for anything. Other devices request the service by being on the same network and entering the local hostname into their browser, which is Oscars-MacBook-Pro.local right now. Potentially could host using AWS later down the line.

The backend is a simple container that retrieves weather data from an api when requested using openmeteo's free, no API key service.

The frontend will call on the backend whenever the user selects a location.

## Security measures
- Https with caddy private certification authority (equivalent to self-cert)
- Basic CORS headers in main.py file using CORSMiddleware
- Basic security headers in Caddyfile
- Reverse proxy with caddy
- Docker isolation
- Rate limiting in fastapi with slowapi


