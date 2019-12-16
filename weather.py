# Python program to find current
# weather details of any city
# using openweathermap api
from BergoladeConfig import *
import requests
from datetime import datetime

api_key = openweather_api_key
base_url = "https://api.openweathermap.org/data/2.5/weather?"


def get_weather(latitude: str, longitude: str):
    print('=====> retrieving weather information')
    complete_url = base_url + "appid=" + api_key + "&lat=" + latitude + "&lon=" + longitude + "&units=metric"

    found_weather = requests.get(complete_url).json()
    #print(found_weather)


    if found_weather["cod"] == "200":

        current_temperature = found_weather["main"]["temp"]
        current_humidiy = found_weather["main"]["humidity"]
        details = found_weather["weather"]
        weather_description = details[0]["description"]
        sunrise = datetime.fromtimestamp(found_weather['sys']['sunrise']).isoformat()
        sunset = datetime.fromtimestamp(found_weather['sys']['sunset']).isoformat()
        report_date = datetime.fromtimestamp(found_weather['dt']).isoformat()
        visibility = found_weather['visibility']
        wind_speed = found_weather['wind']['speed']
        wind_deg = found_weather['wind']['deg']

        weather_data = {
            "weather_report_date": report_date,
            "temperature": current_temperature,
            "humidity": current_humidiy,
            "description": weather_description,
            "sunrise": sunrise,
            "sunset": sunset,
            "visibility": visibility,
            "wind_speed": wind_speed,
            "wind_deg": wind_deg
        }

        # print(weather_data)
        return weather_data

    else:
        print("Error in retrieving weather data: ", found_weather)
        return {}
