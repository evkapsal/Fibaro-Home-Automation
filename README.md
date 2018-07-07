# Fibaro-Home-Automation
For FIbaro Lite/HC2 Python Service.

This Python Service (Running also on Raspberry) can be used to Export Sensors (Devices) and values
 from Fibaro Lite/HCto an Influxdb Database for further actions  like, Grafana Dashboards, Statistics,etc.
Inside .py File you can complete the API/DB details (IP, Usern,Pass, DBName) and you are done.

Dependencies for Python:
  sudo pip install influxdb
  more details here: https://github.com/influxdata/influxdb-python

More Updates and Devices are in Roadmap.

Devices that can be handled (i believe that more can be used not tested):
  1.  Fibaro Motion (Multisensor) Sensor
  2.  Fibaro Dimmer 2
  3.  Power Plug Switch NEO Coolcam
  4.  Smoke Detector NEO Coolcam
  5.  Door Sensor NEO Coolcam and Fibaro
  6.  Remotec AC Infrared Control
  7. TBK-HOME Light Switch Dimmer
  8. Motion Sensor NEO Coolcam

#AZURE IOT HUB Support
New Version with Azure IOT HUB support.
Just insert your Azure IOT Hub Properties in [ImportFibaroItems.py] file and you are ready to send 
IoT messages (JSON) through, IotHub RestAPI.
You can sign up to Microsoft Azure for a free trial  here: https://azure.microsoft.com/en-us/offers/ms-azr-0044p/ 


