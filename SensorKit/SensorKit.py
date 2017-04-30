# SensorKit.py
#
# This is an project for collecting sensor data from grovekit and uploading it to dweet.io
#
'''
The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2017  Dexter Industries

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

from grovepi import grovepi
from grove_rgb_lcd import *
from random import randint
import dweepy
import thread
import time


dht_sensor_port = 8     # Connect the DHt sensor to port 7
dht_sensor_type = 0             # change this depending on your sensor type - see header comment
light_sensor = 1
sound_sensor = 0
button = 3
rotary_sensor = 2
ultrasonic_ranger = 4

#defines
print_id = 0
no_of_sensors = 6
sensor_names = ["Light", "Temp.", "Humidity", "Sound", "Wind dir.", "Range"]
sensor_values = ["0", "0", "0", "0", "0", "0"]

grovepi.pinMode(button, "INPUT")
grovepi.pinMode(rotary_sensor, "INPUT")

light_intensity = ''
button_press = ''
sound_level = ''
temperature = ''
humidity = ''
wind_direction = ''
switch = ''


setText("Initializing..")
setRGB(50, 0, 0)
print_id = 0
start_time = time.time()
initialized = False
data_available = False
time.sleep(1)


while True:

        #init
        if not initialized:
                setRGB(0, 50, 0)
                setText("Getting data..")
                initialized = True

    #Try to read the sensor measurements
    try:
            light_intensity = grovepi.analogRead(light_sensor)
        [temp, hum] = grovepi.dht(dht_sensor_port, dht_sensor_type)
                sound_level = grovepi.analogRead(sound_sensor)
        wind_dir_raw = grovepi.analogRead(rotary_sensor)
                switch = grovepi.digitalRead(button)
                distance = grovepi.ultrasonicRead(ultrasonic_ranger)

        if wind_dir_raw == 0:
            wind_direction = 0
        else:
            wind_direction = wind_dir_raw * (360 / 1024.0)

                wind_direction = float("{0:.1f}".format(wind_direction))

                #Save locally
                sensor_values[0] = light_intensity
                sensor_values[1] = temp
                sensor_values[2] = hum
                sensor_values[3] = sound_level
                sensor_values[4] = wind_direction
                sensor_values[5] = distance

        except (IOError, TypeError) as e:
        print "IO Error"

        #Print to LCD screen
    if switch == 1 and print_id < no_of_sensors:
                print_id +=1
        if print_id >= no_of_sensors:
                print_id = 0


    text = sensor_names[print_id] + ": " + str(sensor_values[print_id]) + "\n"
        #if print_id + 1 < no_of_sensors:
        #        print_id +=1
        #else:
        #        print_id = 0
        text += "(" + str(print_id+1) + "/" + str(no_of_sensors) + ")"
        #text += sensor_names[print_id] + ": " + str(sensor_values[print_id])
        setText(text)

        if not data_available:
                setRGB(50, 50, 50)
                data_available = True

    #Try to dweet it
    try:
        dweepy.dweet_for('OpenData',
                                {'Sound': sound_level,
                                'Light': light_intensity,
                                'Temperature': temp,
                                'Humidity': hum,
                'WindDirection': wind_direction,
                                'Distance': distance,
                'Switch' : switch})

            dweepy.dweet_for('OpenData2',
                                {'Sound': sound_level+randint(0,50),
                                'Light': light_intensity+randint(0,100),
                                'Temperature': temp + +randint(0,5),
                                'Humidity': hum +randint(0,20),
                'WindDirection': wind_direction + randint(0,25),
                                'Distance': distance + randint(0,5),
                'Switch' : switch + +randint(0,1)})

    except:
        print " Dweetio exception"
