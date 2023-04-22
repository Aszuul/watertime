from tkinter import *
import json
from datetime import datetime
import requests
from weatherdataclass import *

# Initialize Window

root = Tk()
root.geometry("400x400")
root.resizable(0,0)
root.title("Garden water notifier")

city_value = StringVar()
state_value = StringVar()

def showWeather():
    api_key = ""
    city_name=city_value.get()
    state_code = state_value.get()
    weather_url='http://api.openweathermap.org/data/2.5/weather?q=' + city_name + ',' + state_code + ',840&appid='+api_key

    response=requests.get(weather_url)
    weather_info=response.json()

    tfield.delete("1.0","end")

    if weather_info['cod'] == 200:
        weatherdata = WeatherData(weather_info,city_name)
        weather = weatherdata.print()
    else:
        weather = f"\n\tWeather for '{city_name}' not found!\n\tKindly Enter valid City Name !!"

    tfield.insert(INSERT, weather)

city_head= Label(root, text = 'Enter City Name', font = 'Arial 12 bold').pack(pady=10) #to generate label heading
 
inp_city = Entry(root, textvariable = city_value,  width = 24, font='Arial 14 bold').pack() #entry field

state_head = Label(root, text = 'Enter State Code', font = 'Arial 12 bold').pack(pady=10)

inp_state = Entry(root, textvariable = state_value,  width = 24, font='Arial 14 bold').pack()

Button(root, command = showWeather, text = "Check Weather", font="Arial 10", bg='lightblue', fg='black', activebackground="teal", padx=5, pady=5 ).pack(pady= 20)

weather_now = Label(root, text = "The Weather is: ", font = 'arial 12 bold').pack(pady=10)
 
tfield = Text(root, width=46, height=10)
tfield.pack()

root.mainloop()
