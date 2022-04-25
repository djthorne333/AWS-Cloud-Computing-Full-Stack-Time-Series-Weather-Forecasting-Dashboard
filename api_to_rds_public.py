import requests
import pandas as pd
import pymysql
from datetime import date
from datetime import datetime


# datetime object containing current date and time
today_time = datetime.now()
# dd/mm/YY H:M:S
today_time = today_time.strftime("%d/%m/%Y %H:%M:%S") + " +0000 UTC"
#print(today_time)


current_weather = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat=xxx&lon=xxx&appid=xxx')
current_weather = current_weather.json()


df_iso = pd.DataFrame([today_time], columns = ['dt_iso'])
df_coord = pd.DataFrame(current_weather['coord'], index=[0])
df_weather = pd.DataFrame(current_weather['weather'], index=[0])
df_base = pd.DataFrame([current_weather['base']], columns=['base'])
df_main = pd.DataFrame(current_weather['main'], index=[0])
df_vis = pd.DataFrame([current_weather['visibility']], columns=['visibility'])
df_wind = pd.DataFrame(current_weather['wind'], index=[0])

#becuase the api request json may not contain the rain or snow keys:
try:
    df_rain = pd.DataFrame(current_weather['rain'], index=[0])
except Exception:
    df_rain = pd.DataFrame([0], columns=['rain_1h'])


try:
    df_snow = pd.DataFrame(current_weather['snow'], index=[0])
except Exception:
    df_snow = pd.DataFrame([0], columns=['snow_1h'])

df_clouds = pd.DataFrame(current_weather['clouds'], index=[0])
df_dt = pd.DataFrame([current_weather['dt']], columns=['dt'])
df_sys = pd.DataFrame(current_weather['sys'], index=[0])
df_tzone = pd.DataFrame([current_weather['timezone']], columns=['timezone'])
df_id = pd.DataFrame([current_weather['id']], columns=['id'])
df_name = pd.DataFrame([current_weather['name']], columns=['name'])
df_cod = pd.DataFrame([current_weather['cod']], columns=['cod'])

#vis is not in excel and dew point hasn't shown up in api request so leaving out those

df = pd.concat([df_dt, df_iso, df_tzone, df_coord['lat'], df_coord['lon'], df_main['temp'], df_main['feels_like'],
                df_main['temp_min'], df_main['temp_max'], df_main['pressure'], df_main['humidity'], df_wind['speed'],
                df_wind['deg'], df_rain, df_snow, df_clouds, df_weather['id'], df_weather['main'],
                df_weather['description'], df_weather['icon']], axis=1)

# print(df.columns)
# pd.set_option("display.max_rows", None, "display.max_columns", None)
# print(df)


# df = pd.read_json(current_weather['main'])

# df = pd.DataFrame(current_weather['main'], index=[0])

# print(df)
#print(df.iloc[0]['temp'])

#Connect to the database
connection = pymysql.connect(host='',
                             user='',
                             password='',
                             database = '',
                             cursorclass=pymysql.cursors.DictCursor)


insert = "insert into bulk values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
#[df.iloc[0][i] for i in df.columns]
connection.cursor().execute(insert, [df.iloc[0][i] for i in df.columns])
connection.commit()