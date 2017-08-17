import spidev
import time
import os
import RPi.GPIO as GPIO
import dht11
import time
import datetime
import http.client
import requests
import minimalmodbus
import request
import serial
SharkMeter = minimalmodbus.Instrument('/dev/serial0', 1) # port name, slave add$
print(SharkMeter)
Whour=SharkMeter.read_long(1099,3,True)
print(Whour)
Voltage=SharkMeter.read_float(999,3,2)
print(Voltage)
AmpA = SharkMeter.read_float(1011,3,2)
print(AmpA)
WTP = SharkMeter.read_float(1017,3,2)
print(WTP)
PFTP = SharkMeter.read_float(1023,3,2)
print(PFTP)

#current=1
current=AmpA
#energy=1
energy=Whour
#power=100
power=Voltage

latitude=2341
longitude=2341
date_time=2421
#pf=1
pf=PFTP
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
  Whour=SharkMeter.read_long(1099,3,True)
print(Whour)
Voltage=SharkMeter.read_float(999,3,2)
print(Voltage)
AmpA = SharkMeter.read_float(1011,3,2)
print(AmpA)
WTP = SharkMeter.read_float(1017,3,2)
print(WTP)
PFTP = SharkMeter.read_float(1023,3,2)
print(PFTP)

#current=1
current=AmpA
#energy=1
energy=Whour
#power=100
power=WTP
pf=PFTP

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
    conn.request("GET","/mysql/dataToDB.php?user=mpardo&pssd=pardo1234&voltage=%s&current=%s&energy=%s&power=%s&latitude=%s&longitude=%s&date_time=%s&temperature=%s&humidity=%s&pf=%s&vbatt1=%s&vbatt2=%s" % (Voltage, current, $
    res = conn.getresponse()


    #Post variables in track.tk

    response = requests.get('http://track-mypower.tk/measurements/internal_conditions/new?temperature_int=%s&humidity_int=%s'%(t, h),
                        auth=requests.auth.HTTPBasicAuth(
                          'admin',
                          'uninorte'))


    response2 = requests.get('http://track-mypower.tk/measurements/electrical/new?voltage_med1=%s&current_med1=%s&energy_med1=%s&power_med1=%s&pf_med1=%s&voltage_batt1=%s&voltage_batt2=%s'%(Voltage, current, energy, power, pf$
                        auth=requests.auth.HTTPBasicAuth(
                          'admin',
                          'uninorte'))

    print(res.reason)
    print("Variables have been updated")

    # Xantrex Control

    #GPIO.setmode(GPIO.BCM)
#GPIO.setup(12, GPIO.OUT)


  #conn = http.client.HTTPSConnection("track-mypower.rhcloud.com")
#conn.request("GET","/control.php")
  #res = conn.getresponse()
  #data = int(res.read())
  #print(data)
  #if data==1:
    #GPIO.output(12,True)
    #time.sleep(2)
    #GPIO.output(12,False)
   # print ("Esta activado")
   # time.sleep(2)
   # print ("Ya no")



    # Wait before repeating loop
    time.sleep(delay)

