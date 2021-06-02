import pyowm

city = "New York, USA"

owm = pyowm.OWM("9b6cbef84565796f8f8e2c2d0f05f5e2")
temp = owm.weather_manager().weather_at_place(city).whether.temprature('celsius')['temp']

print(str(temp))