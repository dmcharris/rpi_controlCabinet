import minimalmodbus
import decimal
from decimal import Decimal

def ReadWHour(SharkMeter, register):
  try:  
    Whour=SharkMeter.read_long(register,3,True)
    Whour=Whour/100
    energy=Whour
    return energy
  except IOError: 
    Whour=0
    energy=Whour
    return energy

def ReadVoltage(SharkMeter, register):
 try:
    Voltage1=SharkMeter.read_float(register,3,2)
    Voltage2=Decimal(Voltage1)
    voltage=round(Voltage2, 2)
    return voltage
 except IOError:
    voltage=0
    return voltage

def ReadCurrent(SharkMeter, register):
  try:
    AmpA1 = SharkMeter.read_float(register,3,2)
    AmpA2 = Decimal(AmpA1)
    AmpA = round(AmpA2, 2)
    current=AmpA
    return current
  except IOError:
    AmpA = 0
    current=AmpA
    return current

def ReadPower(SharkMeter, register):
  try:
    WTP1 = SharkMeter.read_float(register,3,2)
    WTP2 = Decimal(WTP1)
    WTP = round(WTP2, 2)
    power=WTP
    return power
  except IOError:
    WTP = 0
    power=WTP
    return power

def ReadPowerFactor(SharkMeter, register):
  try:
    PFTP1 = SharkMeter.read_float(register,3,2)
    PFTP2 = Decimal(PFTP1)
    PFTP = round(PFTP2, 2)
    pf=PFTP
    return pf
  except IOError:
    PFTP = 0
    pf=PFTP
    return pf