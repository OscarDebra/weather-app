# Fullstack weather app

This is going to be a fullstack weather app, with a python flask backend connecting to a weather api using an api key. The frontend will be in react.

## Architecture

The physical architecture consists of a raspberry pi, other devices request the service by being on the same network and entering the hostname and the ip into their browser. Potentially could host using AWS.

For the backend we are using flask, a simple container that retrieves weather data from an api using an api key when requested. Each new user will need to get their own api key.

The frontend is in react, it calls on the backend whenever the user selects a location.