import re

# Get actual time in text
def time_to_text(words, time):
    H = time.hour
    M = time.minute

    # Start Text
    text = "ES IST"
    led = [words['TEXT']['ES'], words['TEXT']['IST']]
    minutes = 0

    # Space
    text += " "

    # Minutes
    if 0 <= M < 5:
        text += ""
        minutes = M
    elif 5 <= M < 10 or 55 <= M <= 59:
        text += "FÜNF"
        led.append(words['MINUTES']['FUENF'])
        if M < 10:
            minutes = M - 5
        else:
            minutes = M - 55
    elif 10 <= M < 15 or 50 <= M < 55:
        text += "ZEHN"
        led.append(words['MINUTES']['ZEHN'])
        if M < 15:
            minutes = M - 10
        else:
            minutes = M - 50
    elif 15 <= M < 20 or 45 <= M < 50:
        text += "VIERTEL"
        led.append(words['MINUTES']['VIERTEL'])
        if M < 20:
            minutes = M - 15
        else:
            minutes = M - 45
    elif 20 <= M < 25 or 40 <= M < 45:
        text += "ZWANZIG"
        led.append(words['MINUTES']['ZWANZIG'])
        if M < 25:
            minutes = M - 20
        else:
            minutes = M - 40
    elif 25 <= M < 30:
        text += "FUENF VOR HALB"
        led.append(words['MINUTES']['FUENF'])
        led.append(words['TEXT']['VOR'])
        led.append(words['TEXT']['HALB'])
        minutes = M - 25
    elif 30 <= M < 35:
        text += "HALB"
        led.append(words['TEXT']['HALB'])
        minutes = M - 30
    elif 35 <= M < 40:
        text += "FUENF NACH HALB"
        led.append(words['MINUTES']['FUENF'])
        led.append(words['TEXT']['NACH'])
        led.append(words['TEXT']['HALB'])
        minutes = M - 35

    # Space
    text += " "

    # Sign
    if 5 <= M < 25:
        text += "NACH"
        led.append(words['TEXT']['NACH'])
    elif 40 <= M <= 59:
        text += "VOR"
        led.append(words['TEXT']['VOR'])

    # Space
    text += " "

    # Hours
    if M >= 25:
        H += 1

    if H > 12:
        H = H - 12

    if H == 1 and M >= 5:
        text += "EINS"
        led.append(words['HOURS']['EINS'])
    if H == 1 and M < 5:
        text += "EIN"
        led.append(words['HOURS']['EIN'])
    elif H == 2:
        text += "ZWEI"
        led.append(words['HOURS']['ZWEI'])
    elif H == 3:
        text += "DREI"
        led.append(words['HOURS']['DREI'])
    elif H == 4:
        text += "VIER"
        led.append(words['HOURS']['VIER'])
    elif H == 5:
        text += "FÜNF"
        led.append(words['HOURS']['FUENF'])
    elif H == 6:
        text += "SECHS"
        led.append(words['HOURS']['SECHS'])
    elif H == 7:
        text += "SIEBEN"
        led.append(words['HOURS']['SIEBEN'])
    elif H == 8:
        text += "ACHT"
        led.append(words['HOURS']['ACHT'])
    elif H == 9:
        text += "NEUN"
        led.append(words['HOURS']['NEUN'])
    elif H == 10:
        text += "ZEHN"
        led.append(words['HOURS']['ZEHN'])
    elif H == 11:
        text += "ELF"
        led.append(words['HOURS']['ELF'])
    elif H == 12 or H == 0:
        text += "ZWÖLF"
        led.append(words['HOURS']['ZWOELF'])

    # UHR
    if M < 5:
        # Space
        text += " "
        text += "UHR"
        led.append(words['TEXT']['UHR'])

    # Space
    if minutes != 0:
        text += " "

    # Dots
    if minutes == 1:
        text += "PUNKT1"
        led.append(words['MINUTES']['PUNKT1'])
    if minutes == 2:
        text += "PUNKT2"
        led.append(words['MINUTES']['PUNKT2'])
    if minutes == 3:
        text += "PUNKT3"
        led.append(words['MINUTES']['PUNKT3'])
    if minutes == 4:
        text += "PUNKT4"
        led.append(words['MINUTES']['PUNKT4'])

    text = re.sub(' +', ' ', text)
    led = [item for sublist in led for item in sublist]
    return text, led

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
        led = (y + 1) * 11 - x -1

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

    return leds