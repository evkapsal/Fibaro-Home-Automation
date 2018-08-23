# Fibaro-Home-Automation
For Fibaro Lite/HC2 Python Service.

This Python Service (Running also on Raspberry) can be used to Export Sensors (Devices) and values
 from Fibaro Lite/HCto an Influxdb Database for further actions  like, Grafana Dashboards, Statistics,etc.
Inside .py File you can complete the API/DB details (IP, Usern,Pass, DBName) and you are done.

![](https://wcfwfq.am.files.1drv.com/y4mrxWHld37i0HaXU0u3nYKuM_wFofTdbFqsMibkYaqLAN0HV_1dzdVmPeqy29UiHrmD1FgycR6S5os-4kOyItrf8z98bqmcSk_sM1Q2OXMoGwvC_syKgTBAmd8v3QQL0K9qpaTdHqA9CYn3aqs4zpLERd5Xw0h9fVp0rpPLnXASe0IDDxiBllGSMkP-UFhqVdVQmmpmj_Grhz4dCLfs6DphQ?width=1024&height=547&cropmode=none)

**Dependencies for Python:**
  sudo pip install influxdb
  more details here: https://github.com/influxdata/influxdb-python

  sudo pip install mysql-connector-python

  more details here: https://pypi.org/project/mysql-connector-python/ 

 **New*

Integration with Zabbix  https://www.zabbix.com/ and <u>mysql</u> as for network devices bandwidth collection through SNMP.  In order to get this information please go to line #672 and fulfill the object ids. You can easily find the ID's from mySQL - table zabbix_history, example: [SELECT * FROM zabbix.history_uint]. For Grafana there is a plugin for Zabbix details here: https://grafana.com/plugins/alexanderzobnin-zabbix-app

![](https://3satma.am.files.1drv.com/y4mJddmzgyQanqbvBE9Q1B86_N7-8PZ5J6UoiG63zz2K7m9eFkUv9nQ7gFnQCMxDvTMl_7emtwx7azzLGyATNPmSKnY5bWUjncKTwq2rbIRMD7KSS5obvmXFJzQFB7Iko_8Jzm0WSiH1j3PZT-nwX3i0x3aUPVim4JITQN5T6xSYBRs0ajgtgaRjd0vohgbGFVys18Id7RGS2vyhW71zcQZHQ?width=1024&height=519&cropmode=none)

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
5. Serverless Logic App and Service Bus for Notification in mobile/mail/sms/etc
6. Home Behavior Analytics with PCA- Anomaly Detection. Trained Model (In Azure ML Gallery Soon)


**Power BI Pictures**

![](https://vayucg.am.files.1drv.com/y4m7_HLEq7vcaQo9C0L2g4uw_alNnJPXGRW2fH7yvO2RdD_rrakz91lrlXqx4rOJL1IToj_ZWVFY8l45k0731No_x67KAN1a8vK9SC5E_X6s4ssX-_m4EhS5WotsAM2hF1Ou5yQ6P24CSYw9iMAPAQNwI1qaG_EEPeRIWlCEj_A9TIkcdqWlujTI1VAcFEbhP_Wee2ic_lG8AFjKl-djfqaDQ?width=1024&height=553&cropmode=none)

![](https://ghwzaa.am.files.1drv.com/y4m4ND6LsU65qsFZQFc7Nkrvw4np3NtslyhRhqJTAnOF1P3f2zvYLsY-XmMEBInfiOqKP_09iJ3aH3T8KzsDWTg3HX7SSqVKo07-nhAF09iu9tEZL02v3AY-CutCIxQst_2lbcYNgGlO1-j88aU4QuVxbojXKDKBax9ZpGvO9tPfdhuCF92XeyZy7__6YXNKzV65yw7YO9X22ubN_h_DFC0Kg?width=1024&height=568&cropmode=none)

![](https://5qdyxq.am.files.1drv.com/y4mM_KIy3lsww70UmmO4W9EfnOz3avEY7yewZ0MvTqKCt7YGV1cqoRTURr5geg7V1aIBuim3ZRp9jE3uStL0juUxW52xbLrJvhgoPLthRnM4sdXhrDvma6saD838fNm_5CqdXMIX1eRYpbSjSGOntoRpKPElt18YX3AOCezQmB-04czFfVy57fZd7v4cD82piWfofNYiOa8dP2pQ8_We6PmxQ?width=1024&height=547&cropmode=none)

![](https://rx4jga.am.files.1drv.com/y4mNmqyW0aA1GhWpN5gWBFX2--XxeGTe7pid2BlKb_-O2ZpzVkOVmIEewZwHdY6ImX2dP83QnFhAC_5kmwu_cLBGM9YqXWIhdrsJP7qp67cmO43eO-8OT2-8eP5yARsCD5tFEeMhH5w8uWqIZgPgdJHZ3AFEKuHEhbdpskKNEGgZ-_GeZUBzKhIiP3v6jNnOOg_hugZaHt5Q2ikCPr7cfywVw?width=1024&height=588&cropmode=none)

**ROADMAP**

1. **Under Development* Home Behavior Analytics with PCA- Anomaly Detection. Trained Model coming soon...
2. **Under Development* Serverless Function for Device Recognition (Power Consumption)





 


