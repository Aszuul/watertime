from datetime import datetime
kelvin = 273

class WeatherData:
    def __init__(self, weather_info, city_name):
        self.city_name = city_name
        self.temp = int(temp_convert(weather_info['main']['temp']))
        self.feels_like_temp = int(temp_convert(weather_info['main']['feels_like']))
        self.pressure = weather_info['main']['pressure']
        self.humidity = weather_info['main']['humidity']
        self.wind_speed = weather_info['wind']['speed'] * 3.6
        self.sunrise = weather_info['sys']['sunrise']
        self.sunset = weather_info['sys']['sunset']
        self.timezone = weather_info['timezone']
        self.cloudy = weather_info['clouds']['all']
        self.description = weather_info['weather'][0]['description']

        self.sunrise_time = time_format_for_location(self.sunrise + self.timezone)
        self.sunset_time = time_format_for_location(self.sunset + self.timezone)
    
    def print(self):
        return f"\nWeather of: {self.city_name}\nTemperature (F): {self.temp}°\nFeels like in (F): {self.feels_like_temp}°\nPressure: {self.pressure} hPa\nHumidity: {self.humidity}%\nSunrise at {self.sunrise_time} and Sunset at {self.sunset_time}\nCloud: {self.cloudy}%\nInfo: {self.description}"

def time_format_for_location(utc_with_tz):
    local_time = datetime.utcfromtimestamp(utc_with_tz)
    return local_time.time()

def temp_convert(temp):
    return (temp - kelvin) * 9/5 + 32
