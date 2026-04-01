'''this project uses REST API to fetch live updates of weather from weatherAPI 
the responses are recieved in json format which are then coverted into python dictionary for compiler friendly
then the required field like temp and condition are extracted and displayed'''

import requests     #it is used to fetch data from web API as i took from the weather api 
from plyer import notification   #this imports notification feature(plyer helps python interact with systems feature i.e OS like notification battery)
import time                      #time library from python packages

#Take input from user for safety of API key
API_KEY = input("Enter your API key: ")    #weatherAPI
CITY = input("Enter city name: ")

URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"   

def get_weather():
    try:
        response = requests.get(URL)     #sends request to API which sends back the weather data
        data = response.json()           #json format-dictionary weatherAPI returns the data in json format which then .json() converts it into python dictionary format 

        #Proper error handling BEFORE accessing data
        if data.get("cod") != 200:
            print("Error:", data.get("message"))
            return None

        #extraction of data temp and weather description like haze or sunny
        temp = data["main"]["temp"]
        weather = data["weather"][0]["description"]

        #condition to add emoji feature to make it more attractive
        cond = weather.lower()     #lower method used we don't know in which type of case the text will come from weatherAPI(SUNNY,Sunny,sunny) so keep an universal, used lower().
        if "haze" in cond:
            emoji = "💨"
        elif "sunny" in cond or "clear" in cond:
            emoji = "⛅"
        elif "rain" in cond:
            emoji = "☔"
        else:
            emoji = ""

        return temp, weather, emoji

    #exception handling
    except Exception as e:
        print("Network/Error:", e)
        return None


#First run (same as your original flow)
result = get_weather()

if result:    #to check if all the arguments are provided
    temp, weather, emoji = result

    print(f"Temperature: {temp}°C")
    print(f"Weather: {emoji} {weather}")

    #desktop notification
    notification.notify(
        title="Weather Update",
        message=f"Temp: {temp}°C\nCondition: {emoji} {weather}",
        timeout=10
    )


#or else use for i in range(1):[for limited times]
while True:     #to run it in loop 
    result = get_weather()

    if result:
        temp, weather, emoji = result

        #call the notification method to display notification on desktop
        notification.notify(  
            title="🌦️Live Weather Update",
            message=f"{CITY}\nTemp: {temp}°C\n{emoji} {weather}",
            timeout=10
        )

    time.sleep(1800)  # 30 minutes (shows notification in every 30 minutes)