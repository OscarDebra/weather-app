import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://Oscars-MacBook-Pro.local"], 
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)



def get_weather():
	# Setup the Open-Meteo API client with cache and retry on error
	cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
	retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
	openmeteo = openmeteo_requests.Client(session = retry_session)

	# Make sure all required weather variables are listed here
	# The order of variables in hourly or daily is important to assign them correctly below
	url = "https://api.open-meteo.com/v1/forecast"
	params = {
		"latitude": 59.20,
		"longitude": 10.76,
		"hourly": "temperature_2m",
		"timezone": "auto",
	}
	return openmeteo.weather_api(url, params = params)



def get_temp():
	responses = get_weather()

	# Process first location. Add a for-loop for multiple locations or weather models
	response = responses[0]
	print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
	print(f"Elevation: {response.Elevation()} m asl")
	print(f"Timezone: {response.Timezone()}{response.TimezoneAbbreviation()}")
	print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

	# Process hourly data. The order of variables needs to be the same as requested.
	hourly = response.Hourly()
	hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

	hourly_data = {
		"date": pd.date_range(
			start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
			end =  pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
			freq = pd.Timedelta(seconds = hourly.Interval()),
			inclusive = "left"
		).tz_convert(response.Timezone().decode())
	}

	hourly_data["temperature_2m"] = hourly_temperature_2m

	hourly_dataframe = pd.DataFrame(data = hourly_data)
	hourly_dataframe["date"] = hourly_dataframe["date"].astype(str)

	print("temp values:", hourly_temperature_2m[:5])
	print("type:", type(hourly_temperature_2m[0]))

	return hourly_dataframe.to_dict(orient="records")



@app.get("/api/health")
@limiter.limit("10/minute")
def root(request: Request):
	return {"message": "Weather API is running"}



@app.get("/api/weather")
@limiter.limit("10/minute")
def weather(request: Request):
	data = get_temp()
	return {"hourly": data}



@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests"}
    )