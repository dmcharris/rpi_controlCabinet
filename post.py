import http.client
import requests
def Post(vect):
 # res = conn.getresponse()
     
    #Sent=Vectorize(voltage, current, energy, power, t, h, pf, vbank1, vbank2, radprom, sptemp,spvol,spcurr)
    #Post variables in track.tk

  response = requests.get('http://track-mypower.tk/measurements/internal_conditions/new?temperature_int=%s&humidity_int=%s'%(vect[4], vect[5]),
                    auth=requests.auth.HTTPBasicAuth(
                      'admin',
                      'uninorte'))


  response2 = requests.get('http://track-mypower.tk/measurements/electrical/new?voltage_med1=%s&current_med1=%s&energy_med1=%s&power_med1=%s&pf_med1=%s&voltage_batt1=%s&voltage_batt2=%s'%(vect[0], vect[1], vect[2], vect[3],vect[6], vect[7], vect[8]),
                    auth=requests.auth.HTTPBasicAuth(
                      'admin',
                      'uninorte'))
  response3 = requests.get('http://track-mypower.tk/measurements/panel_conditions/new?temp_ext=%s&temp_panel=%s&radiation=%s&current_panel=%s&voltage_panel=%s'%(vect[4],vect[10],vect[9],vect[12],vect[11]),
                    auth=requests.auth.HTTPBasicAuth(
                      'admin',
                      'uninorte'))
  print("Variables have been updated") 