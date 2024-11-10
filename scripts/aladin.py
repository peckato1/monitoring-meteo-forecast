import dataclasses
import dataclass_csv
import datetime
import os
import requests
import pytz
import sys


LATITUDE = os.getenv("LATITUDE")
LONGITUDE = os.getenv("LONGITUDE")
URL = "https://aladinonline.oblacno.cz/get_data.php?latitude={LATITUDE}&longitude={LONGITUDE}"


@dataclasses.dataclass
class DataPoint:
    time: str
    forecast_time: str

    temperature: float
    apparent_temperature: float
    humidity: float
    pressure: float

    precipitation_snow: float
    precipitation_total: float

    clouds_low: float
    clouds_medium: float
    clouds_high: float
    clouds_total: float

    wind_speed: float
    wind_direction: float
    wind_gust_direction: float
    wind_gust_speed: float


def format_datetime(timestamp: datetime.datetime):
    return timestamp.strftime("%Y-%m-%dT%H:%M:%S%z")


if not LATITUDE or not LONGITUDE:
    print("Please set LATITUDE and LONGITUDE environment variables.")
    sys.exit(1)


resp = requests.get(URL.format(LATITUDE=LATITUDE, LONGITUDE=LONGITUDE))
resp.raise_for_status()
data = resp.json()


forecast_time = datetime.datetime.strptime(data["forecastTimeIso"], "%Y-%m-%d %H:%M:%S").astimezone(pytz.timezone("Europe/Prague"))
parameters = data["parameterValues"]


datapoints = [DataPoint(
    time=format_datetime(forecast_time + datetime.timedelta(hours=i)),
    forecast_time=format_datetime(forecast_time),
    pressure=parameters["PRESSURE"][i],
    apparent_temperature=parameters["APPARENT_TEMPERATURE"][i],
    temperature=parameters["TEMPERATURE"][i],
    humidity=parameters["HUMIDITY"][i],
    precipitation_total=parameters["PRECIPITATION_TOTAL"][i],
    precipitation_snow=parameters["PRECIPITATION_SNOW"][i],
    clouds_low=parameters["CLOUDS_LOW"][i],
    clouds_medium=parameters["CLOUDS_MEDIUM"][i],
    clouds_high=parameters["CLOUDS_HIGH"][i],
    clouds_total=parameters["CLOUDS_TOTAL"][i],
    wind_gust_direction=parameters["WIND_GUST_DIRECTION"][i],
    wind_gust_speed=parameters["WIND_GUST_SPEED"][i],
    wind_speed=parameters["WIND_SPEED"][i],
    wind_direction=parameters["WIND_DIRECTION"][i]
    ) for i in range(data["forecastLength"])]


w = dataclass_csv.DataclassWriter(sys.stdout, datapoints, DataPoint)
w.write()
