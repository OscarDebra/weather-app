import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry
from fastapi import FastAPI

app = FastAPI()

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
		"timezone": "Europe/Berlin",
	}
	responses = openmeteo.weather_api(url, params = params)

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

@app.get("/")
def root():
	return {"message": "Weather API is running"}

@app.get("/weather")
def weather():
	data = get_weather()
	print("Hello")
	return {"hourly": data}