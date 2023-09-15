import badger2040
import badger_os
import urequests
import ntptime

from display import draw_temp, draw_humid, draw_compass, draw_wind_info, draw_precipication

POSITION = (59.9138, 10.7387)
UPDATES_PER_HOUR = 4

USER_AGENT = 'Pimoroni Badger 2040W'


def nowcast(position):
    try:
        url = f'https://api.met.no/weatherapi/nowcast/2.0/complete?lat={position[0]}&lon={position[1]}'
        res = urequests.get(url=url, headers={'User-Agent': USER_AGENT})
        return res.json()['properties']['timeseries'][0]['data']['instant']['details']
    except Exception as ex:
        raise Exception('Failed to retrieve weather data', ex)


def draw_all(
        display,
        temperature,
        humidity,
        wind_from_direction,
        wind_speed,
        wind_speed_of_gust,
        precipitation_rate
):
    display.set_pen(15)
    display.clear()
    display.set_pen(0)

    display.line(100, 0, 100, 127, 2)
    display.line(0, 63, 100, 63, 2)
    display.line(100, 96, 296, 96, 2)

    draw_temp(display, temperature, 0)
    draw_humid(display, humidity, 68)
    draw_compass(display, wind_from_direction, 147, 45)
    draw_wind_info(display, wind_speed, wind_speed_of_gust, 195, 0)
    draw_precipication(display, precipitation_rate, 106, 106)

    display.update()


def init():
    try:
        badger = badger2040.Badger2040()
        badger.set_update_speed(badger2040.UPDATE_NORMAL)
        return badger
    except Exception as ex:
        raise Exception('Failed to initialize', ex)


def connect(display):
    try:
        display.connect(status_handler=None)
    except Exception as ex:
        raise Exception('Failed to connect to WIFI', ex)


def set_time():
    try:
        ntptime.settime()
    except Exception as ex:
        raise Exception('Failed to set time', ex)


def run():
    state = {
        'cycles': 0,
        'errors': 0
    }

    try:
        badger = init()

        badger_os.state_load('weather', state)

        connect(badger)
        set_time()

        state['cycles'] = state['cycles'] + 1
        state['last_time'] = ntptime.time()

        badger_os.state_save('weather', state)

        details = nowcast(POSITION)

        draw_all(
            badger,
            details['air_temperature'],
            details['relative_humidity'],
            details['wind_from_direction'],
            details['wind_speed'],
            details['wind_speed_of_gust'],
            details['precipitation_rate']
        )

        badger2040.sleep_for(int(60 / UPDATES_PER_HOUR))
    except Exception as ex:
        print(ex)

        state['errors'] = state['errors'] + 1
        state['last_error'] = str(ex)
        state['last_error_time'] = ntptime.time()
        badger_os.state_save('weather', state)

        badger2040.sleep_for(1)


if __name__ == '__main__':
    run()
