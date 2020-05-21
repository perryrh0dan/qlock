import re

# Get actual time in text


def time_to_text(words, time):
    H = time.hour
    M = time.minute

    # Start Text
    text = "ES IST"
    word_leds = [words['TEXT']['ES'], words['TEXT']['IST']]
    corner_leds = []
    minutes = 0

    # Space
    text += " "

    # Minutes
    if 0 <= M < 5:
        text += ""
        minutes = M
    elif 5 <= M < 10 or 55 <= M <= 59:
        text += "FÜNF"
        word_leds.append(words['MINUTES']['FUENF'])
        if M < 10:
            minutes = M - 5
        else:
            minutes = M - 55
    elif 10 <= M < 15 or 50 <= M < 55:
        text += "ZEHN"
        word_leds.append(words['MINUTES']['ZEHN'])
        if M < 15:
            minutes = M - 10
        else:
            minutes = M - 50
    elif 15 <= M < 20 or 45 <= M < 50:
        text += "VIERTEL"
        word_leds.append(words['MINUTES']['VIERTEL'])
        if M < 20:
            minutes = M - 15
        else:
            minutes = M - 45
    elif 20 <= M < 25 or 40 <= M < 45:
        text += "ZWANZIG"
        word_leds.append(words['MINUTES']['ZWANZIG'])
        if M < 25:
            minutes = M - 20
        else:
            minutes = M - 40
    elif 25 <= M < 30:
        text += "FUENF VOR HALB"
        word_leds.append(words['MINUTES']['FUENF'])
        word_leds.append(words['TEXT']['VOR'])
        word_leds.append(words['TEXT']['HALB'])
        minutes = M - 25
    elif 30 <= M < 35:
        text += "HALB"
        word_leds.append(words['TEXT']['HALB'])
        minutes = M - 30
    elif 35 <= M < 40:
        text += "FUENF NACH HALB"
        word_leds.append(words['MINUTES']['FUENF'])
        word_leds.append(words['TEXT']['NACH'])
        word_leds.append(words['TEXT']['HALB'])
        minutes = M - 35

    # Space
    text += " "

    # Sign
    if 5 <= M < 25:
        text += "NACH"
        word_leds.append(words['TEXT']['NACH'])
    elif 40 <= M <= 59:
        text += "VOR"
        word_leds.append(words['TEXT']['VOR'])

    # Space
    text += " "

    # Hours
    if M >= 25:
        H += 1

    if H > 12:
        H = H - 12

    if H == 1 and M >= 5:
        text += "EINS"
        word_leds.append(words['HOURS']['EINS'])
    elif H == 1 and M < 5:
        text += "EIN"
        word_leds.append(words['HOURS']['EIN'])
    elif H == 2:
        text += "ZWEI"
        word_leds.append(words['HOURS']['ZWEI'])
    elif H == 3:
        text += "DREI"
        word_leds.append(words['HOURS']['DREI'])
    elif H == 4:
        text += "VIER"
        word_leds.append(words['HOURS']['VIER'])
    elif H == 5:
        text += "FÜNF"
        word_leds.append(words['HOURS']['FUENF'])
    elif H == 6:
        text += "SECHS"
        word_leds.append(words['HOURS']['SECHS'])
    elif H == 7:
        text += "SIEBEN"
        word_leds.append(words['HOURS']['SIEBEN'])
    elif H == 8:
        text += "ACHT"
        word_leds.append(words['HOURS']['ACHT'])
    elif H == 9:
        text += "NEUN"
        word_leds.append(words['HOURS']['NEUN'])
    elif H == 10:
        text += "ZEHN"
        word_leds.append(words['HOURS']['ZEHN'])
    elif H == 11:
        text += "ELF"
        word_leds.append(words['HOURS']['ELF'])
    elif H == 12 or H == 0:
        text += "ZWÖLF"
        word_leds.append(words['HOURS']['ZWOELF'])

    # UHR
    if M < 5:
        # Space
        text += " "
        text += "UHR"
        word_leds.append(words['TEXT']['UHR'])

    # Space
    if minutes != 0:
        text += " "

    # Dots
    if minutes == 1:
        text += "PUNKT1"
        corner_leds.append(words['MINUTES']['PUNKT1'])
    if minutes == 2:
        text += "PUNKT2"
        corner_leds.append(words['MINUTES']['PUNKT2'])
    if minutes == 3:
        text += "PUNKT3"
        corner_leds.append(words['MINUTES']['PUNKT3'])
    if minutes == 4:
        text += "PUNKT4"
        corner_leds.append(words['MINUTES']['PUNKT4'])

    text = re.sub(' +', ' ', text)
    word_leds = [item for sublist in word_leds for item in sublist]
    corner_leds = [item for sublist in corner_leds for item in sublist]
    return text, word_leds, corner_leds


def calculate_brightness(config, brightness):
    max_brightness_percentage = config['max_brightness_percentage']
    min_brightness_percentage = config['min_brightness_percentage']
    max_brightness_threshold = config['max_brightness_threshold']
    min_brightness_threshold = config['min_brightness_threshold']

    percentage = (brightness - min_brightness_threshold) / \
        (max_brightness_threshold - min_brightness_threshold)

    if percentage > 1:
        return max_brightness_percentage
    elif percentage < 0:
        return min_brightness_percentage
    else:
        return (max_brightness_percentage - min_brightness_percentage) * percentage + min_brightness_percentage


def get_leds_xy(x, y, length, direction):
    leds = []

    if length <= 0:
        return leds

    led = 0
    if y % 2 == 0:
        led = y * 11 + x
    else:
        led = (y + 1) * 11 - x - 1

    if led <= 109:
        leds.append(led)
    else:
        return leds

    if direction == "y":
        for i in range(length - 1):
            led = 0
            if (y + i) % 2 == 0:
                led = leds[i] + 21 - 2 * x
            else:
                led = leds[i] + 21 - 2 * (10 - x)

            if led <= 109:
                leds.append(led)
            else:
                break

    leds = list(filter(lambda x: x >= 0, leds))
    return leds
