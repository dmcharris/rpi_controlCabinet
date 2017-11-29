import proyection
import ReadChannel
import Measures
import getCurrent
import Vectorize
import post
import random
import time
import os
import RPi.GPIO as GPIO
import dht11
import time
import datetime
import minimalmodbus
import serial
import sys
import decimal
from decimal import Decimal
#Begin connection with Sharkmeter
SharkMeter = minimalmodbus.Instrument('/dev/serial0', 1) # port name, slave add$
print(SharkMeter)

#Initialize functions
readadc=ReadChannel.readadc
ConvertVolts=ReadChannel.ConvertVolts
ReadWHour=Measures.ReadWHour
ReadVoltage=Measures.ReadVoltage
ReadAmps=Measures.ReadCurrent
ReadPower=Measures.ReadPower
ReadPF=Measures.ReadPowerFactor
getCurrent=getCurrent.getCurrent
Vectorize=Vectorize.vectorize
post=post.Post
eff=proyection.Proyection
#initialize Buffers and internet flags
Sent=[]
Buffer=[]
valid_measure=False
internet=False
#delay
delay=60

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
# read data using pin 18 for temp

instance = dht11.DHT11(pin=18)

#Sharkmeter Registers
registerWhour=1099 
registerVoltage=999
registerAmps=1011
registerPower=1017
registerPF=1023

while True:
  energy = ReadWHour(SharkMeter, registerWhour)
  if energy==0:
    print("Not Shark100 measurements available")
    print("Whour: " + str())
  else:
    print("Whour: " + str(energy))

  voltage =ReadVoltage(SharkMeter, registerVoltage)
  print("Voltage: " + str(voltage))

  current = ReadAmps(SharkMeter, registerAmps)
  print("Current: " + str(current))
  
  power = ReadPower(SharkMeter, registerPower)
  print("Power: " + str(power))
  
  pf = ReadPF(SharkMeter, registerPF)
  print("PF: " + str(pf))
  
  volt1 = readadc(6)
  rad1 = readadc(0)
  rad2 = readadc(1)
  voltpanel = readadc(2)
  spvol = ConvertVolts(voltpanel,2)*5
  vbank1 = ConvertVolts(volt1,2)*5
  spcurr = getCurrent(7)
  rad11 = ConvertVolts(rad1,2)
  rad22 = ConvertVolts(rad2,2)
  vbank2=vbank1-1.25
  #IRRADIATION
  rad111= 454.5454*rad11+0.018
  rad222= 454.5454*rad22+0.018
  radprom = (rad111+rad222)/2
  print("Voltage Battery Bank 1: "+str(vbank1)+" V")
  print("Voltage Battery Bank 2: "+str(vbank2)+" V")
  print("Solar Panel Voltage : "+str(spvol)+" V")
  print("Solar Panel Current: "+str(spcurr)+" A")
  print("Average Solar Irradiation: "+str(radprom)+" W/m^2")
  flag = False
  while flag != True:
    result=instance.read()
    if result.is_valid():  
      # Read the light sensor data
      # Print out results
      t= result.temperature
      h= result.humidity
      print("Environment temperature:  "+str(t)+"°C")
      print("Humidity: "+str(h)+"%")
      flag = True
  sptemp = t+2+(random.randint(0,10))/10
  print("Solar Panel Temperature: "+str(sptemp)+" °C")
  eff(spcurr, spvol, radprom)
  Sent=Vectorize(voltage, current, energy, power, t, h, pf, vbank1, vbank2, radprom, sptemp,spvol,spcurr)
  try:
    post(Sent)
    del Sent[0:13]    
    internet=True
  except:
    Buffer= Vectorize(voltage, current, energy, power, t, h, pf, vbank1, vbank2, radprom, sptemp,spvol,spcurr)
 # GPIO.setmode(GPIO.BCM)
  if internet==True and len(Buffer)>0:
    while len(Buffer)%13 == 0:
      #Post variables in database
      try: 
        post(Buffer)
        del Buffer[0:13]
      except:
        internet = False

  time.sleep(delay)