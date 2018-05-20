# Fibaro-Home-Automation
For FIbaro Lite/HC2 Python Service.

This Python Service (Running also on Raspberry) can be used to Export Sensors (Devices) and values
 from Fibaro Lite/HCto an Influxdb Database for further actions  like, Grafana Dashboards, Statistics,etc.
Inside .py File you can complete the API/DB details (IP, Usern,Pass, DBName) and you are done.

Dependencies for Python:
  sudo pip install influxdb
  more details here: https://github.com/influxdata/influxdb-python

More Updates and Devices are in Roadmap.

Devices can be handled:
  1.  Fibaro Motion (Multisensor) Sensor
  2.  Fibaro Dimmer 2
  3.  Power Plug Switch AEON
  4.  Smoke Detector AEON
  5.  Door Sensor AEON
  6.  Remotec AC Infrared Control
