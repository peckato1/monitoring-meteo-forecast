import dataclasses
import dataclass_csv
import datetime
import os
import requests
import pytz
import sys


LATITUDE = os.getenv("LATITUDE")
LONGITUDE = os.getenv("LONGITUDE")
OPENWEATHER_APIKEY = os.getenv("OPENWEATHER_APIKEY")
URL = "https://api.openweathermap.org/data/2.5/weather?units=metric&lat={LATITUDE}&lon={LONGITUDE}&appid={OPENWEATHER_APIKEY}"


@dataclasses.dataclass
class DataPoint:
    time: str

    temperature: float
    temperature_min: float
    temperature_max: float
    temperature_feel: float
    humidity_percent: float
    pressure_sea_level: float
    pressure_ground_level: float
    visibility: float
    wind_speed: float
    wind_direction: float
    wind_gust_speed: float
    clouds_percentage: float
    rain_1h: float|None = None
    snow_1h: float|None = None


def format_datetime(timestamp: datetime.datetime):
    return timestamp.strftime("%Y-%m-%dT%H:%M:%S%z")


if not LATITUDE or not LONGITUDE or not OPENWEATHER_APIKEY:
    print("Please set LATITUDE and LONGITUDE and OPENWEATHER_APIKEY environment variables.")
    sys.exit(1)


resp = requests.get(URL.format(LATITUDE=LATITUDE, LONGITUDE=LONGITUDE, OPENWEATHER_APIKEY=OPENWEATHER_APIKEY))
resp.raise_for_status()
data = resp.json()


# from unix timestamp
timepoint = datetime.datetime.fromtimestamp(data["dt"], tz=pytz.utc).astimezone(pytz.timezone("Europe/Prague"))
datapoint = DataPoint(
    time=format_datetime(timepoint),
    temperature=data["main"]["temp"],
    temperature_min=data["main"]["temp_min"],
    temperature_max=data["main"]["temp_max"],
    temperature_feel=data["main"]["feels_like"],
    humidity_percent=data["main"]["humidity"],
    pressure_sea_level=data["main"]["sea_level"] * 100,
    pressure_ground_level=data["main"]["grnd_level"] * 100,
    visibility=data["visibility"],
    wind_speed=data["wind"]["speed"],
    wind_direction=data["wind"]["deg"],
    wind_gust_speed=data["wind"]["gust"],
    clouds_percentage=data["clouds"]["all"],
    rain_1h=data.get("rain", dict()).get("1h", 0),
    snow_1h=data.get("snow", dict()).get("1h", 0),
)


w = dataclass_csv.DataclassWriter(sys.stdout, [datapoint], DataPoint)
w.write()
