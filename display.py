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
