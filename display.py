from math import cos, sin


def segments(number):
    if number == '0':
        return 'ABCDEF'
    elif number == '1':
        return 'BC'
    elif number == '2':
        return 'ABDEG'
    elif number == '3':
        return 'ABCDG'
    elif number == '4':
        return 'BCFG'
    elif number == '5':
        return 'ACDFG'
    elif number == '6':
        return 'ACDEFG'
    elif number == '7':
        return 'ABC'
    elif number == '8':
        return 'ABCDEFG'
    elif number == '9':
        return 'ABCDFG'
    elif number == '-':
        return 'G'
    elif number == '.':
        return ''


def pixels(segment):
    if segment == 'A':
        return [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0)]
    elif segment == 'B':
        return [(5, 1), (6, 1), (5, 2), (6, 2), (5, 3), (6, 3), (5, 4), (6, 4), (5, 5), (6, 5)]
    elif segment == 'C':
        return [(5, 7), (6, 7), (5, 8), (6, 8), (5, 9), (6, 9), (5, 10), (6, 10), (5, 11), (6, 11)]
    elif segment == 'D':
        return [(1, 12), (2, 12), (3, 12), (4, 12), (5, 12)]
    elif segment == 'E':
        return [(0, 7), (1, 7), (0, 8), (1, 8), (0, 9), (1, 9), (0, 10), (1, 10), (0, 11), (1, 11)]
    elif segment == 'F':
        return [(0, 1), (1, 1), (0, 2), (1, 2), (0, 3), (1, 3), (0, 4), (1, 4), (0, 5), (1, 5)]
    elif segment == 'G':
        return [(1, 6), (2, 6), (3, 6), (4, 6), (5, 6)]


def draw_char(display, char, size, xo, yo):
    for s in segments(char):
        if s is not None:
            for p in pixels(s):
                for y in range(0, size):
                    for x in range(0, size):
                        rx = xo + p[0] * size + x
                        ry = yo + p[1] * size + y

                        display.pixel(rx, ry)


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
