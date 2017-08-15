import http.client
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

while 1>0:
  conn = http.client.HTTPSConnection("track-mypower.rhcloud.com")
  conn.request("GET","/control.php")
  res = conn.getresponse()
  data = int(res.read())
  print(data)
  
  #Corto
  if data==1:   
    GPIO.output(12, True)
    time.sleep(2)
    GPIO.output(12,False)
    

  time.sleep(2)
    

  


