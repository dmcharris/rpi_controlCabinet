import spidev
import time
import os
import RPi.GPIO as GPIO
import dht11
import time
import datetime
import http.client

current=1
energy=1
power=100
latitude=2341
longitude=2341
date_time=2421
pf=1
vbatt1=12
vbatt2=12
# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# read data using pin 14
instance = dht11.DHT11(pin=18)

# SPI bus
spi = spidev.SpiDev()
spi.open(0,0)

# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7

def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data
# Function to convert data to voltage level,
# rounded to specified number of decimal places.
def ConvertVolts(data,places):
  volts = (data * 3.3) / float(1023)
  volts = round(volts,places)
  return volts


# Define sensor channels
pot = 0

# Define delay between readings
delay = 3

while True:
  result=instance.read()
  if result.is_valid():
    # Read the light sensor data
    adc = ReadChannel(pot)
    pot_volts = ConvertVolts(adc,2)
 # Print out results
    print ("--------------------------------------------")
    print ("Lectura ADC: ", adc)
    print("Voltaje: {}V".format(pot_volts))
    t= result.temperature
    h= result.humidity
    print("Temperatura:  "+str(t)+"C")
    print("Humedad: "+str(h)+"%")

    #Post variables in database

    conn = http.client.HTTPSConnection("track-mypower.rhcloud.com")
    conn.request("GET","/mysql/dataToDB.php?user=mpardo&pssd=pardo1234&voltage=%s&current=%s&energy=%s&power=%s&latitude=%s&longitude=%s&date_time=%s&temperature=%s&hu$
    res = conn.getresponse()
    print(res.reason)


    # Wait before repeating loop
    time.sleep(delay)
