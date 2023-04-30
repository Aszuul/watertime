import requests
import mysecrets

class geo_data:
    def __init__(self,city_name,state_code,country_code) -> 'geolocation':
        self.city_name = city_name
        self.state_code = state_code
        self.country_code = country_code

        res = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&limit=1&appid={mysecrets.api_key}")
        geodata = res.json()
        
        self.lat = geodata[0]["lat"]
        self.lon = geodata[0]["lon"]
        