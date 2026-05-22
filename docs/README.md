# Installation and setup

1. Run `git clone https://github.com/OscarDebra/weather-app.git` to clone the project on your device.
2. Run `docker compose up --build` while in the weather-app folder to build the project on the device.
3. To verify it's working visit the backend container on the device where the container is hosted by searching `http://localhost:80`.
4. To open the container on another device, find the ip of the device where the container is hosted, then visit `http://[ip]`

# User guide

This project currently only has a backend container with 2 api endpoints.

1. To verify if the app is working on your device, first make sure you are on the same network, then visit `http://[ip]`, where the ip is the ip of the device where the container is hosted.
2. The second endpoint is located at `http://[ip]/weather` and currently returns the projected temperature each hour for the next week at a very specific location.

# About the project

This is going to be a fullstack weather app, with a python fastapi backend connecting to a weather api. The frontend will be in react.

## Architecture

The physical architecture consists of a raspberry pi, but can be substituted for anything, other devices request the service by being on the same network and entering the ip into their browser. Potentially could host using AWS.

For the backend we are using fastapi, a simple container that retrieves weather data from an api when requested.

The frontend is in react, it calls on the backend whenever the user selects a location.
