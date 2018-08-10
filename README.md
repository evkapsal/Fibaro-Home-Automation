# Fibaro-Home-Automation
For Fibaro Lite/HC2 Python Service.

This Python Service (Running also on Raspberry) can be used to Export Sensors (Devices) and values
 from Fibaro Lite/HCto an Influxdb Database for further actions  like, Grafana Dashboards, Statistics,etc.
Inside .py File you can complete the API/DB details (IP, Usern,Pass, DBName) and you are done.

![](https://1drv.ms/u/s!AkXyhV_E0LGhl-s9WIRQQO9Ysr987g)

**Dependencies for Python:**
  sudo pip install influxdb
  more details here: https://github.com/influxdata/influxdb-python

  sudo pip install mysql-connector-python

  more details here: https://pypi.org/project/mysql-connector-python/ 

 **New*

Integration with Zabbix  https://www.zabbix.com/ and <u>mysql</u> as for network devices bandwidth collection through SNMP.  In order to get this information please go to line #672 and fulfill the object ids. You can easily find the ID's from mySQL - table zabbix_history, example: [SELECT * FROM zabbix.history_uint]. For Grafana there is a plugin for Zabbix details here: https://grafana.com/plugins/alexanderzobnin-zabbix-app

![](https://1drv.ms/u/s!AkXyhV_E0LGhl-s7MUshYCaTRooxdA)

More Updates and Devices are in Roadmap.

Devices that are used (i believe that more can be used **not tested*):
    1.  Fibaro Motion (Multisensor) Sensor **(z-wave)*
    2.  Fibaro Dimmer 2 **(z-wave)*
    3.  Power Plug Switch NEO Coolcam **(z-wave)*
    4.  Smoke Detector NEO Coolcam **(z-wave)*
    5.  Door Sensor NEO Coolcam and Fibaro **(z-wave)*
    6.  Remotec AC Infrared Control **(z-wave)*
    7.  TBK-HOME Light Switch Dimmer **(z-wave)*
    8.  Motion Sensor NEO Coolcam **(z-wave)*
    9.  Philio Temperature/Humidity Sensor **(z-wave)*
    10.  Swiid Inter Cord Switch **(z-wave)*

**AZURE IOT HUB Support**
New Version with Azure IOT HUB support.
Just insert your Azure IOT Hub Properties in [ImportFibaroItems.py] file and you are ready to send 
IoT messages (JSON) through, IotHub RestAPI.
You can sign up to Microsoft Azure for a free trial  here: https://azure.microsoft.com/en-us/offers/ms-azr-0044p/ 

Microsoft Azure Services that being used:

1. Azure IOT Hub.
2. Azure Stream Analytics.
3. Azure Machine Learning.
4. Azure Functions.
5. Azure Table Storage.
6. Azure Logic App.
7. Azure Service Bus.

**Updated Version*

1. New json Object Format (Integration for Azure Machine Learning)
2. Azure Stream Analytics Queries for Table Storage and Power BI API.
3. Home Network Bandwidth new Object for analytics and visualization.
4. Power BI API Support 

![](https://1drv.ms/u/s!AkXyhV_E0LGhl-s8K9IpM2yd6Cme7Q)

![](https://1drv.ms/u/s!AkXyhV_E0LGhl-s_XJSqnz3OIIztTw)

![](https://1drv.ms/u/s!AkXyhV_E0LGhl-s-j3RJhxNAVmZy0g)

![](https://1drv.ms/u/s!AkXyhV_E0LGhl-tA1hrNyzKgqLjAYQ)

**ROADMAP**

1. **Under Development* Home Behavior Analytics with PCA- Anomaly Detection. Trained Model coming soon...
2. **Under Development* Serverless Function for Device Recognition (Power Consumption)
3. **Under Development* Serverless Logic App and Service Bus for Notification in mobile/mail/sms/etc..





 


