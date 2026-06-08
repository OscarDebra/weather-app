# Admin guide

## Installation and setup

1. Run `git clone https://github.com/OscarDebra/weather-app.git` to clone the project on your device.
2. Create a new file in root called .env and copy over the contents of the .env.example file inside it, then replace the secret key with a long string of random characters (32-64 characters). You can, for example run the command `openssl rand -hex 32` to create a secret key of length 32.
3. Run `docker compose up --build` while in the weather-app folder to build the project on the device.
4. To verify it's working visit the backend container on the device where the container is hosted by searching `http://localhost`.
5. To open the container on another device, find the ip of the device where the container is hosted, then visit `http://http://Oscars-MacBook-Pro.local`
6. Create an admin user by first going into the create_admin.py file found in the /app directory in the /backend directory, change the password variable to your own password. Next run the create_admin.py file by running `docker compose exec backend python -m app.create_admin`. You will need to log in with this user to access protected endpoints.
7. To shut it down, run `docker compose down`
8. To turn it back on at a later time, run `docker compose up`, you do not need to rebuild each time.


# User guide

1. To verify if the app is working on your device, first make sure you are on the same network, then visit `http://Oscars-MacBook-Pro.local`, this is the frontend, which currently is empty.
2. Some endpoints require no permissions, meaning you do not need to provide a valid access token in the http header, the rest require user or admin permissions.

### No permission enpoints
- The health endpoint can be reached at `http://Oscars-MacBook-Pro.local/api/health` and displays a message if the backend is up.
- The login enpoint can be reached in the terminal by running `https://oscars-macbook-pro.local/api/login \      
  -H "Content-Type: application/json" \
  -d '{"username":"USERNAME","password":"PASSWORD"}'`, make sure to replace the username and password with an existing account. This gives you an access token, which you will need to reach all protected endpoints, whether the account you're logging into is an admin account or not changes which endpoints you can reach.

### User endpoints
- The weather endpoint can be reached in the terminal by running `curl -k https://oscars-macbook-pro.local/api/weather \            
-H "Authorization: Bearer TOKEN"`, make sure you replace TOKEN with the token you received by logging into your account. This endpoint currently returns the projected temperature each hour for the next week at a very specific location.

### Admin endpoints
- The create account endpoint can be used in the terminal by running `curl -k -X POST https://oscars-macbook-pro.local/api/admin/create_user \
-H "Authorization: Bearer TOKEN" \
-H "Content-Type: application/json" \
-d '{
  "username":"USERNAME",
  "password":"PASSWORD",
  "is_admin":ISADMIN
}'`, making sure to replace the TOKEN, USERNAME, PASSWORD and ISADMIN fields. This creates a new user that can be used while calling the login endpoint to receive an authentication token.
- The users endpoint can be reached in the terminal by running `curl -k https://oscars-macbook-pro.local/api/admin/users \        
  -H "Authorization: Bearer TOKEN`, making sure to replace the TOKEN field. THis returns a list of the users that currently exist within the database.
"



# About the project

This project consists of three docker containers. One frontend container in react, a backend container using fastapi and a caddy container.

The physical architecture consists of a raspberry pi, but is currently hosted on a macbook while under development, but the raspi can be substituted for anything. Other devices request the service by being on the same network and entering the local hostname into their browser, which is Oscars-MacBook-Pro.local right now.

## Backend container

The backend is a simple container that retrieves weather data from an api when requested using openmeteo's free, no API key service.

The /data directory contains the databases needed for this project, right now that's just the users database, which stores users login info.

The /app directory contains all the python code.

The dockerfile build the container in the /code directory, and installs the dependencies defined in the requirements.txt folder.

## Security measures
- Https with caddy private certification authority (equivalent to self-certificate)
- Basic CORS headers in main.py file using CORSMiddleware
- Basic security headers in Caddyfile
- Reverse proxy with caddy
- Docker isolation
- Rate limiting in fastapi with slowapi
- Protected endpoints that require regular or admin permissions

# Debugging

1. Users database persists after docker shutdown, to wipe the users database, run `docker compose exec backend python app/reset_db.py`, this runs a special python script found in the /app folder for the backend directory that wipes and restarts the users database.
2. To enter any container and confirm their contents, run `docker exec -it <container name> bash`, to exit, type exit in the terminal window or type CTRL + d 
3. To view the status of the containers, run `docker compose ps`

