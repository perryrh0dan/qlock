<h1 align="center">
  QLock
</h1>

<h4 align="center">
  Word clock powered by raspberrypi and python
</h4>

<div align="center">
  <img alt="cover" width="70%" src="media/title.jpg" />
</div>

## Description

## Highlights

## Contents

- [Description](#description)
- [Highlights](#highlights)
- [Install](#install)
- [Usage](#usage)
- [Configuration](#configuration)
- [Images](#images)
- [Development](#development)
- [Team](#team)
- [License](#license)

## Install

Run following command to install all dependencies
``` bash
pip install -r requirements.txt
```

## Usage

## Configuration

to configure qlock modify the config.json in the root directory. The following illustrates all the available options with their respective default values.

``` json
{
    "color": [255, 255, 255],
    "dates": [{
        "date": "21.06",
        "text": "HAPPYBIRTHDAYPAPA"
    }, {
        "date": "19.04",
        "text": "HAPPYBIRTHDAYMAMA"
    }]
}
```

### In Detail

#### color

- Type: String
- Default: [255, 255, 255]

Color of the LEDs.

#### dates

- Type: Array
- Default: []

Special Dates like birthdays can be configured here. The clock will write the given text at this date to the screen.

## Images

<div align="center">
  <img alt="cover" width="70%" src="media/holes.jpg" />
</div>

<div align="center">
  <img alt="cover" width="70%" src="media/first_leds.jpg" />
</div>

<div align="center">
  <img alt="cover" width="70%" src="media/all_leds.jpg" />
</div>

<div align="center">
  <img alt="cover" width="70%" src="media/first_light.jpg" />
</div>

<div align="center">
  <img alt="cover" width="70%" src="media/back_plate.jpg" />
</div>

<div align="center">
  <img alt="cover" width="70%" src="media/cutting.jpg" />
</div>

<div align="center">
  <img alt="cover" width="70%" src="media/front_plate.jpg" />
</div>

<div align="center">
  <img alt="cover" width="70%" src="media/finish.jpg" />
</div>

## Development

For local development on a non raspberry pi system you have to comment out the controller import. Because the GPIO packages are only available on a raspberry pi.

## Team

- Thomas Pöhlmann [(@perryrh0dan)](https://github.com/perryrh0dan)

## License

[MIT](https://github.com/perryrh0dan/qlock/blob/master/license.md)

