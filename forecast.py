import requests
import mysecrets

class forecast_data:
    # api.openweathermap.org/data/2.5/forecast/daily?lat={lat}&lon={lon}&cnt={cnt}&appid={API key}
    def __init__(self,geo_data):
        res = requests.get(f"https://api.openweathermap.org/data/2.5/forecast/daily?lat={geo_data.lat}&lon={geo_data.lon}&cnt=5&appid={mysecrets.api_key}")
        forecast_data = res.json()


# class daily_data: 
#     def __init__(self) -> None:
#         self.