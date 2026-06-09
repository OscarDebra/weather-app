# Installation and setup

1. Run `git clone https://github.com/OscarDebra/weather-app.git` to clone the project on your device.
2. Create a new file in root called .env and copy over the contents of the .env.example file inside it, then replace the secret key with a long string of random characters (32-64 characters). You can, for example run the command `openssl rand -hex 32` to create a secret key of length 32. After that you can delete the .env.example file if you want by doing `rm .env.example`.
3. You need to match the hostname in the caddyfile to the hostname of your device, run `sudo nano /etc/hosts` in the terminal and enter your password to view hosts. There should be one that begins with 127.0.1.1 and ends with a hostname like "oscars-macbook-pro". Copy that hostname and paste it in the place of HOSTNAME in the Caddyfile found in root, also paste it in the field that says HOSTNAME in the main.py file found in the /backend/app directory.
4. Run `docker compose up --build` while in the weather-app folder to build the project on the device.
5. To open the container on another device, visit `https://HOSTNAME.local`, where you replace HOSTNAME with the hostname you entered in the caddyfile.
6. Create an admin user by first going into the create_admin.py file found in the /app directory in the /backend directory, change the password variable to your own password. Next run the create_admin.py file by running `docker compose exec backend python -m app.create_admin`. You will need to log in with this user by hitting the login endpoint defined below to receive an access token to access the protected endpoints defined below as well.
7. To shut it down, run `docker compose down`
8. To turn it back on at a later time, run `docker compose up`, you do not need to rebuild each time.


# User guide

1. To verify if the app is working on your device, first make sure you are on the same network, then visit `http://HOSTNAME.local`, ask your admin if you do not know the hostname. This is the frontend, which currently is empty.
2. Some endpoints require no permissions, meaning you do not need to provide a valid access token in the http header, the rest require user or admin permissions. If you do not have an account, ask your admin to make you one.

### No permission enpoints

- The health endpoint can be reached at `curl -k https://HOSTNAME.local/api/health` and displays a message if the backend is up.
- The login enpoint can be reached in the terminal by running `curl -k "https://HOSTNAME.local/api/login" -H "Content-Type: application/json" -d '{"username":"USERNAME","password":"PASSWORD"}'`, make sure to replace the username and password with an existing account. This gives you an access token, which you will need to reach all protected endpoints, whether the account you're logging into is an admin account or not changes which endpoints you can reach.

### User endpoints

- User accounts can use the weather app.

- The weather endpoint can be reached in the terminal by running `curl -k https://HOSTNAME.local/api/weather -H "Authorization: Bearer TOKEN"`, make sure you replace TOKEN with the token you received by logging into your account. This endpoint currently returns the projected temperature each hour for the next week at a very specific location.

### Admin endpoints

- Admin endpoints can only be accessed with a token given by logging into an admin account. Admins can create and administer accounts as well as everything that user accounts can.

- The create account endpoint can be used in the terminal by running `curl -k -X POST https://HOSTNAME.local/api/admin/create_user -H "Authorization: Bearer TOKEN" -H "Content-Type: application/json" -d '{"username":"USERNAME", "password":"PASSWORD", "is_admin":ISADMIN}'`, making sure to replace the TOKEN, USERNAME, PASSWORD and ISADMIN fields, type 1 or 0 for ISADMIN. This creates a new user that can be used while calling the login endpoint to receive an authentication token. 
- The users endpoint can be reached in the terminal by running `curl -k "https://HOSTNAME.local/api/admin/users" -H "Authorization: Bearer TOKEN"`, making sure to replace the TOKEN field. THis returns a list of the users that currently exist within the database.
- The delete users endpoint can be reached in the terminal by running `curl -k -X DELETE https://weather-app.local/api/admin/users -H "Authorization: Bearer TOKEN" -H "Content-Type: application/json" -d '{"username":"USERNAME"}'`, making sure to replace the TOKEN and USERNAME field.
- The replace password endpoint can be reached in the terminal by running `curl -k -X PUT https://weather-app.local/api/admin/users/password -H "Authorization: Bearer TOKEN" -H "Content-Type: application/json" -d '{"username":"USERNAME", "new_password":"NEWPASSWORD"}'`, making sure to replace the TOKEN, USERNAME and NEWPASSWORD fields.

# Debugging

1. Users database persists after docker shutdown, to wipe the users database, run `docker compose exec backend python app/reset_db.py`, this runs a special python script found in the /app folder for the backend directory that wipes and restarts the users database.
2. To enter any container and confirm their contents, run `docker exec -it <container name> bash`, to exit, type exit in the terminal window or type CTRL + d 
3. To view the status of the containers, run `docker compose ps`

# About the project

This project consists of three docker containers. One frontend container in react, a backend container using fastapi and a caddy container.

The physical architecture consists of a raspberry pi, but the raspi can be substituted for anything. Other devices request the service by being on the same network and entering the local hostname into their browser.

## Backend container

The backend is a simple container that retrieves weather data from an api when requested using openmeteo's free, no API key service.

The /data directory contains the databases needed for this project, right now that's just the users database, which stores users login info.

The /app directory contains all the python code.

The dockerfile build the container in the /code directory, and installs the dependencies defined in the requirements.txt folder.

## Frontend container

Frontend container currently only has a basic vite react template.

## Caddy container

The caddy container serves https through its own autogenerated certificate authority. It also works as a reverse proxy, redirecting user traffic through the frontend and backend container.

## Security measures
- Https with caddy private certification authority (equivalent to self-certificate)
- Basic CORS headers in main.py file using CORSMiddleware
- Basic security headers in Caddyfile
- Reverse proxy with caddy
- Docker isolation
- Rate limiting in fastapi with slowapi
- Protected endpoints that require regular or admin permissions

# Privacy Policy

This application is privately hosted by its operator. There is no commercial data sharing. Only sensitive authentication data is stored (passwords, JWTs), ask your local system operator if you wish to have data deleted. 

### Login data

When a user is created, the system stores the following in the local users.db sqlite database:

- Username
- Password (stored as a secure hash)
- Admin status (boolean flag)

### Authentication Data

When users log in, the system issues a JSON Web Token (JWT) containing:

- Username (as the token subject)
- Expiration timestamp

The token is used to authenticate protected endpoints.
Tokens expire by default after 24h, can be manually manipulated inside the .env file.
No session history is stored server-side.

### Deletion

Data can be deleted in the following ways:

- Deleting the users.db file
- Reinitializing the database using the provided reinitialization script

