import badger2040
import badger_os
import urequests
import ntptime

POSITION = (59.9138, 10.7387)
UPDATES_PER_HOUR = 4

USER_AGENT = 'Pimoroni Badger 2040W'

from math import cos, sin
from display import draw_char


def draw_comma(display, size, xo, yo):
    for y in range(0, size):
        for x in range(0, size):
            display.pixel(x + xo, y + yo)


def draw_celsius(display, xo, yo):
    display.image(
        bytearray(
            (
                0b10000001,
                0b00111100,
                0b11111100,
                0b11111100,
                0b11111100,
                0b11111100,
                0b00111100,
                0b10000001,
            )
        ),
        8,
        8,
        xo,
        yo,
    )


def draw_percent(display, xo, yo):
    display.image(
        bytearray(
            (
                0b00111000,
                0b10011000,
                0b11001000,
                0b11100111,
                0b00010011,
                0b00011001,
                0b00011100,
                0b11111111,
            )
        ),
        8,
        8,
        xo,
        yo,
    )


def draw_temp(display, temp, yo):
    display.set_font('bitmap8')
    display.text('Temp', 0, yo)

    is_negative = temp < 0

    temp_str = '{:.1f}'.format(abs(temp))

    whole = '' + temp_str[0:temp_str.index('.')]
    frac = '' + temp_str[temp_str.index('.') + 1:]

    if len(whole) == 1:
        if is_negative:
            draw_char(display, '-', 3, 24, yo + 18)

        draw_char(display, whole[0], 3, 48, yo + 18)
    else:
        if is_negative:
            draw_char(display, '-', 3, 0, yo + 18)

        draw_char(display, whole[0], 3, 24, yo + 18)
        draw_char(display, whole[1], 3, 48, yo + 18)

    draw_comma(display, 3, 70, yo + 54)
    draw_celsius(display, 80, yo + 18)
    draw_char(display, frac, 2, 76, yo + 31)


def draw_humid(display, humid, yo):
    display.set_font('bitmap8')
    display.text('Luftfukt', 0, yo)

    humid_str = '{:.1f}'.format(humid)

    whole = '' + humid_str[0:humid_str.index('.')]
    frac = '' + humid_str[humid_str.index('.') + 1:]

    if len(whole) == 1:
        draw_char(display, humid_str[0], 3, 48, yo + 18)
    else:
        draw_char(display, humid_str[0], 3, 24, yo + 18)
        draw_char(display, humid_str[1], 3, 48, yo + 18)

    draw_comma(display, 3, 70, yo + 54)
    draw_percent(display, 80, yo + 18)
    draw_char(display, frac, 2, 76, yo + 31)


def draw_arrow(display, angle, xo, yo):
    angle = angle / 57.29

    result = []

    for vertex in [(-5, -25), (0, -20), (5, -25), (2, 15), (8, 12), (0, 25), (-8, 12), (-2, 15)]:
        x = vertex[0]
        y = vertex[1]

        result.append(
            (round(x * cos(angle) - y * sin(angle)) + xo, round(x * sin(angle) + y * cos(angle)) + yo))

    display.polygon(result)


def draw_compass(display, angle, xo, yo):
    display.set_pen(0)
    display.circle(xo, yo, 30)
    display.set_pen(15)
    display.circle(xo, yo, 28)
    display.set_pen(0)
    display.set_font('bitmap8')
    display.text('N', xo - 4, yo - 46, 0)
    display.text('NV', xo - 30, yo - 30, 0, 0.5)
    display.text('NØ', xo + 24, yo - 30, 0, 0.5)
    display.text('S', xo - 4, yo + 33, 0)
    display.text('SV', xo - 30, yo + 25, 0, 0.5)
    display.text('SØ', xo + 24, yo + 25, 0, 0.5)
    display.text('V', xo - 40, yo - 7, 0)
    display.text('Ø', xo + 33, yo - 7, 0)
    draw_arrow(display, angle, xo, yo)


def draw_wind_info(display, average, gust, xo, yo):
    display.set_font('bitmap8')
    display.text('Gj.snitt', xo, yo)
    display.text(f'{average} m/s', 195, yo + 22)
    display.text('I kastene', xo, yo + 54)
    display.text(f'{gust} m/s', xo, yo + 76)


def draw_precipication(display, rate, xo, yo):
    display.text(f'Nedbør {rate} mm/t', xo, yo)


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
    except Exeption as ex:
        raise Exception('Failed to set time', ex)


def run():
    try:
        badger = init()

        state = {
            'cycles': 0,
            'errors': 0
        }

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





