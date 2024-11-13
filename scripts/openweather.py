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
    humidity_percent: int
    pressure_sea_level: int
    pressure_ground_level: int
    visibility: int
    wind_speed: float
    wind_direction: float
    wind_gust_speed: float
    clouds_percent: int
    rain_1h: float
    snow_1h: float


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
    temperature=float(data["main"]["temp"]),
    temperature_min=float(data["main"]["temp_min"]),
    temperature_max=float(data["main"]["temp_max"]),
    temperature_feel=float(data["main"]["feels_like"]),
    humidity_percent=int(data["main"]["humidity"]),
    pressure_sea_level=int(data["main"]["sea_level"] * 100),
    pressure_ground_level=int(data["main"]["grnd_level"] * 100),
    visibility=int(data["visibility"]),
    wind_speed=float(data["wind"]["speed"]),
    wind_direction=int(data["wind"]["deg"]),
    wind_gust_speed=float(data["wind"]["gust"]),
    clouds_percent=int(data["clouds"]["all"]),
    rain_1h=float(data.get("rain", dict()).get("1h", 0)),
    snow_1h=float(data.get("snow", dict()).get("1h", 0)),
)


w = dataclass_csv.DataclassWriter(sys.stdout, [datapoint], DataPoint)
w.write()
