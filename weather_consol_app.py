from pyowm import OWM
import datetime

city = "Erevan"

owm = OWM("9b6cbef84565796f8f8e2c2d0f05f5e2")
mgr = owm.weather_manager()
observation = mgr.weather_at_place(city)
w = observation.weather

# temp_cels = w.temperature('celsius')['temp']
# temp_far = w.temperature('fahrenheit')['temp']

# Температура
temp = w.temperature('celsius')
temp_cels = temp['temp']
temp_feels = temp['feels_like']
temp_max = temp['temp_max']
temp_min = temp['temp_min']

# Скорость ветра
wind = w.wind()['speed']

# Влажность
humi = w.humidity

# Облачность
# clouds = w.clouds

# Статус
status = w.status

# Детали
# det = w.detailed_status

# Время
time = w.reference_time('iso')

# Давление
pressure = w.pressure['press']

# Видимость
vis_dis = w.visibility_distance

# Продолжительность дня
sunrise_time = datetime.datetime.fromtimestamp(w.sunrise_time())
sunset_time = datetime.datetime.fromtimestamp(w.sunset_time())
length_of_the_day = sunset_time - sunrise_time


code_to_smile = {
    "Clear": "Ясно \U00002600",
    "Clouds": "Облачно \U00002601",
    "Rain": "Дождь \U00002614",
    "Drizzle": "Дождь \U00002614",
    "Thunderstorm": "Гроза \U000026A1",
    "Snow": "Снег \U0001F328",
    "Mist": "Туман \U0001F32B"
}

# print("tempriture in celsius = " + str(temp_cels) + "\ntempriture in farengate = " + str(temp_far))
print(
	f"Время: {time}\n"
    f"В городе {city} температура: {temp_cels}C°, ощущается как: {temp_feels}C°\n"
	f"Максимальная температура: {temp_max}C°, минимальная температура: {temp_min}C°.\n"
    f"Скорость ветера: {wind}м/с\n"
    f"Влажность: {humi}%\n"
	f"Давление: {pressure} мм.рт.ст\n"
    f"Восход солнца: {sunrise_time}\nЗакат солнца: {sunset_time}\nПродолжительность дня: {length_of_the_day}\n"
    f"Видимость: {vis_dis} м\n"
	f"Статус: {code_to_smile[status]}"
)
