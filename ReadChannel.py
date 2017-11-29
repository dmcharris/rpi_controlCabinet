import spidev

spi = spidev.SpiDev()
spi.open(0,0)

# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7

def readadc(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data

def ConvertVolts(data,places):
  volts = (data * 3.4) / float(1023)
  volts = round(volts,places)
  return volts
