import requests
import mysecrets
from datetime import *

class forecast_data:
    # api.openweathermap.org/data/2.5/forecast/daily?lat={lat}&lon={lon}&cnt={cnt}&appid={API key}
    def __init__(self,geo_data):
        res = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?lat={geo_data.lat}&lon={geo_data.lon}&appid={mysecrets.api_key}")
        forecast_data = res.json()
        self.forecast = []
        for w in forecast_data['list']:
            self.forecast.append(daily_data(w['dt'],w))

    def print(self):
        res = ''
        for d in self.forecast:
            res += d.print() + "\n"
        
        return res

    def when_to_water(self):
        today = datetime.now()
        res = ''
        for w in self.forecast:
            if w.weather == "Rain":
                rain_in = str(w.day - today)
                if (w.day - today) < timedelta(days=2):
                    res = f"rain in {rain_in}. You may be able to wait."
                else:
                    res = f"rain in {rain_in}. You should water."
                break
            else:
                res = "No rain expected in the next 5 days. You should water."

        return res

class daily_data: 
    def __init__(self,day,forecast) -> None:
        self.day = datetime.fromtimestamp(day)
        self.weather = forecast['weather'][0]['main']
    
    def print(self):
        return f"{self.day.strftime('%a %d %b %Y, %H:%M')}: Weather is {self.weather}"
    
