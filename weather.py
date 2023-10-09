import pprint
import requests

from matplotlib import pyplot as plt
from datetime import datetime

DEG_F = 'f'
DEF_C = 'c'


def to_fahrenheit(K):
    return round((float(K) - 273.15) * 1.8000 + 32.00)


def to_celcius(K):
    return round(float(K) - 273.15)


def formatter(dates):
    def get_dates(x):
        try:
            return dates[int(x)]
        except:
            return ""

    def fmt(x):
        dt = datetime.fromisoformat(get_dates(x))
        if dt.hour == 0 or x == 0 or x == len(dates) - 1:
            return dt.strftime("%b %d %#I %p")
        else:
            return dt.strftime("%#I %p")
    return lambda x, pos: fmt(x)


def get_regional_weather(region, units=DEG_F):
    # 'c22a9bc763f87b271b966016007372f6' Scott
    # '28cc5fe56aa246f9409d5a0b4fbcb5ac' Mine
    API_KEY = 'c22a9bc763f87b271b966016007372f6'
    API_URL = f"https://api.openweathermap.org/data/2.5/forecast?appid={
        API_KEY}&q={region}"

    req = requests.get(API_URL)
    response = req.json()

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(response)


get_regional_weather('South Carolina')

forecast_list = response['list']

dates = []
temps = []

temp_formatter = to_fahrenheit if units is DEG_F else to_celcius

for forecast in forecast_list:
    date = forecast['dt_txt']
    temp = temp_formatter(forecast['main']['feels_like'])
    dates.append(date)
    temps.append(temp)

    print(temps)
    print(dates)

    return dates, temps, units


def plot_data(region, dates, temps, units):
    temp_unit = 'Fahrenheit' if units is DEG_F else 'Celcius'

    plt.title(f"The hourly temperature forecast for {region} in {temp_unit}")
    plt.plot(dates, temps)

    plt.xlabel('Dates')
    plt.ylabel(f'Temperature in {temp_unit}')

    ax = plt.gca()
    ax.xaxis.set_major_formatter(formatter(dates))

    plt.tick_params(axis='x', labelrotation=90)
    plt.show()

    def main():
        region = input(
            'Weather Forecaster\n\nFor what region do you want weather? ')
        data = None
        if len(region) == 0 or region.upper() == 'NONE':
            print('sorry for asking')
            exit()
        try:
            data = get_regional_weather(region)
        except (ValueError, PermissionError) as e:
            print(str(e))
            exit()
        except:
            print('Sorry - could not find region')
            exit()
        else:
            print('Generating your forecast...')
            plot_data(region, *data)


if __name__ == '__main__':
    main()

region = 'Las Vegas'
get_regional_weather(region)
plot_data(region, *data)
