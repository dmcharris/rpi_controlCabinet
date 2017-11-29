def Proyection(curr, vol, rad):
  a=1.7  
  radn=rad/1000
  i=curr/12
  v=vol/20
  n=(v*i)/(radn*a)
  proy=n*rad
  print("Panel efficiency = "+str(n*100))
  print("Energy proyection = "+str(proy))