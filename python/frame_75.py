#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""This module displays some info on the 7.5 inch e-ink display"""
import sys
import os
import datetime
import logging
import epd7in5_V2
from PIL import Image,ImageDraw,ImageFont
import weather_check as weather

fontdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'fonts')

logging.basicConfig(level=logging.DEBUG)

FONT64 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 64)
FONT36 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 36)
FONT28 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 28)
FONT18 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 18)
FONT14 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 14)
FONT11 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 11)

WEATHER_ICON = ImageFont.truetype(os.path.join(fontdir,'meteocons.ttf'), 64)

WEATHER_ICON_MAP_DAY = {
1000 : "B", 1003 : "H", 1006 : "N", 1009 : "Y",
1030 : "J", 1063 : "Q", 1066 : "U", 1069 : "U",
1072 : "U", 1087 : "Z", 1114 : "V", 1117 : "W",
1135 : "M", 1147 : "M", 1150 : "Q", 1153 : "Q",
1168 : "X", 1171 : "X", 1180 : "Q", 1183 : "Q",
1189 : "R", 1192 : "R", 1195 : "R", 1198 : "Q",
1201 : "R", 1204 : "U", 1207 : "W", 1210 : "V",
1213 : "V", 1216 : "W", 1219 : "W", 1222 : "W",
1225 : "W", 1237 : "X", 1240 : "Q", 1243 : "R",
1246 : "R", 1249 : "U", 1252 : "W", 1255 : "V",
1258 : "W", 1261 : "X", 1264 : "X", 1273 : "Q",
1276 : "R", 1279 : "U", 1282 : "W"
}

WEATHER_ICON_MAP_NIGHT = {
1000 : "C", 1003 : "I", 1006 : "N", 1009 : "Y",
1030 : "K", 1063 : "Q", 1066 : "U", 1069 : "U",
1072 : "U", 1087 : "Z", 1114 : "V", 1117 : "W",
1135 : "M", 1147 : "M", 1150 : "Q", 1153 : "Q",
1168 : "X", 1171 : "X", 1180 : "Q", 1183 : "Q",
1189 : "R", 1192 : "R", 1195 : "R", 1198 : "Q",
1201 : "R", 1204 : "U", 1207 : "W", 1210 : "V",
1213 : "V", 1216 : "W", 1219 : "W", 1222 : "W",
1225 : "W", 1237 : "X", 1240 : "Q", 1243 : "R",
1246 : "R", 1249 : "U", 1252 : "W", 1255 : "V",
1258 : "W", 1261 : "X", 1264 : "X", 1273 : "Q",
1276 : "R", 1279 : "U", 1282 : "W"  
}

def main():
    """Main Method, updates the display stats"""
    try:
        logging.info("Running Plex Display")

        epd = epd7in5_V2.EPD()
        logging.info("init and Clear")
        epd.init()
        epd.Clear()

        logging.info("Clearing display...")
        image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(image)

        #storing time
        time = datetime.datetime.now()

        #time
        draw.text((2, 2), f"{time.strftime('%H:%M')}", font = FONT36, fill = 0)

        #date
        draw.text((100, 2), f"{time.strftime('%a %d %b')}", font = FONT36, fill = 0)

        draw.rectangle([(0,0),(96, 44)],outline = 0)

        #weather
        weather_client = weather.WeatherClient()
        current_weather = weather.get_current(weather_client)

        #check if day or night
        if current_weather['current']['is_day'] == 1:
            draw.text((2, 100), WEATHER_ICON_MAP_DAY[current_weather["current"]["condition"]["code"]], font = WEATHER_ICON, fill = 0)
        else :
            draw.text((2, 100), WEATHER_ICON_MAP_NIGHT[current_weather["current"]["condition"]["code"]], font = WEATHER_ICON, fill = 0)
        draw.text((68, 100), f"{current_weather['current']['temp_c']}\N{DEGREE SIGN}C", font = FONT28, fill = 0)
        draw.text((68, 130), current_weather["current"]["condition"]["text"], font = FONT28, fill = 0)

        draw.text((2, 400), f"I LOVE", font = FONT64, fill = 0)
        draw.text((2, 470), f"BARRY", font = FONT64, fill = 0)

        image = image.rotate(180) # rotate
        epd.display(epd.getbuffer(image))

    except KeyboardInterrupt:
        logging.info("ctrl + c:")
        epd7in5_V2.epdconfig.module_exit()
        sys.exit()

if __name__ == "__main__":
    main()