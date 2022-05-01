#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""This module displays some info on the 7.5 inch e-ink display"""
import sys
import os
import datetime
import logging
import configparser
import epd7in5_V2
from PIL import Image,ImageDraw,ImageFont
import weather_check as weatherCheck
import bus_check as busCheck

FONTDIR = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'fonts')

CONFIG_FILE = os.path.join(os.path.dirname(__file__),"config.cfg")

logging.basicConfig(level=logging.DEBUG)

FONT64 = ImageFont.truetype(os.path.join(FONTDIR, 'Font.ttc'), 64)
FONT36 = ImageFont.truetype(os.path.join(FONTDIR, 'Font.ttc'), 36)
FONT28 = ImageFont.truetype(os.path.join(FONTDIR, 'Font.ttc'), 28)
FONT22 = ImageFont.truetype(os.path.join(FONTDIR, 'Font.ttc'), 22)
FONT18 = ImageFont.truetype(os.path.join(FONTDIR, 'Font.ttc'), 18)
FONT14 = ImageFont.truetype(os.path.join(FONTDIR, 'Font.ttc'), 14)
FONT11 = ImageFont.truetype(os.path.join(FONTDIR, 'Font.ttc'), 11)

WEATHER_ICON = ImageFont.truetype(os.path.join(FONTDIR,'meteocons.ttf'), 64)

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

def read_config(section):
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config[section]

def bus_times(draw):
    bus_config = read_config("Bus")
    step_y = 24

    #bus 1
    logging.info(f'Bus stop number - {bus_config["Bus1"]}')
    bus_data = busCheck.get_bus(bus_config["Bus1"])
    start_y = 644
    draw.rectangle([(286,642),(376, 790)],outline = 0)
    draw.line([(286, 668),(466, 668)])
    draw.text((290, start_y), "Church", font = FONT22, fill = 0)
    start_y += step_y
    temp_count = 0
    for bus in bus_data:
        if bus[0] > 0 and temp_count < 5:
            draw.text((290, start_y), str(bus[0]) + "m", font = FONT22, fill = 0)
            draw.text((340, start_y), bus[1], font = FONT11, fill = 0)
            draw.text((340, start_y+11), bus[2], font = FONT11, fill = 0)
            start_y += step_y
            temp_count += 1
    
    #bus 2
    logging.info(f'Bus stop number - {bus_config["Bus2"]}')
    bus_data = busCheck.get_bus(bus_config["Bus2"])
    start_y = 644
    draw.rectangle([(376,642),(466, 790)],outline = 0)
    draw.text((380, start_y), "Cross", font = FONT22, fill = 0)
    start_y += step_y
    temp_count = 0
    for bus in bus_data:
        if bus[0] > 0 and temp_count < 5:
            draw.text((380, start_y), str(bus[0]) + "m", font = FONT22, fill = 0)
            draw.text((430, start_y), bus[1], font = FONT11, fill = 0)
            draw.text((430, start_y+11), bus[2], font = FONT11, fill = 0)
            start_y += step_y
            temp_count += 1

def main():
    """Main Method, updates the display stats"""
    try:
        logging.info("Running Display")

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
        weather_client = weatherCheck.WeatherClient()
        current_weather = weatherCheck.get_current(weather_client)

        #check if day or night
        if current_weather['current']['is_day'] == 1:
            draw.text((2, 100), WEATHER_ICON_MAP_DAY[current_weather["current"]["condition"]["code"]], font = WEATHER_ICON, fill = 0)
        else :
            draw.text((2, 100), WEATHER_ICON_MAP_NIGHT[current_weather["current"]["condition"]["code"]], font = WEATHER_ICON, fill = 0)
        draw.text((68, 100), f"{current_weather['current']['temp_c']}\N{DEGREE SIGN}C", font = FONT28, fill = 0)
        draw.text((68, 130), current_weather["current"]["condition"]["text"], font = FONT28, fill = 0)

        bus_times(draw)

        image = image.rotate(180) # rotate
        epd.display(epd.getbuffer(image))

    except KeyboardInterrupt:
        logging.info("ctrl + c:")
        epd7in5_V2.epdconfig.module_exit()
        sys.exit()

if __name__ == "__main__":
    main()