
import requests
import json
import calendar
import time
from influxdb import InfluxDBClient
import logging
import datetime

#Fibaro Appliance
hcl_host = "YOUR-FIBARO-IP"
hcl_user = 'YOUR-FIBARO-USER'
hcl_password = 'YOUR-FIBARO-PASSWORD'


#influxdb access data
host = "YOUR-INFLUXDB-IP"
port = "8086"
user = "YOUR-INFLUXDB-USER"
password = "YOUR-INFLUXDB-PASSWORD"
dbname = "YOUR-INFLUXDB-DATABASE-NAME"


def sendIOTmessage (message):
    
    #Connection Settings
    deviceID = "YOUR-IOTHUB-DEVICEID"
    iotHubAPIVer = "2018-04-01"
    iotHubRestURI = "https://[YOUR-IOT-HUB-URL]/devices/" + deviceID + "/messages/events?" + "api-version=" + iotHubAPIVer
    SASToken = 'YOUR-SAS-TOKEN'

    Headers = {}
    Headers['Authorization'] = SASToken
    Headers['Content-Type'] = "application/json"

    idatetime =  datetime.datetime.now()
    body = {}
    body['datetime'] = str(idatetime)
    body['deviceClient'] = deviceID
    body['Message'] = message

    # Send Message
    try:
        resp = requests.post(iotHubRestURI, json=body, headers=Headers)
        #print(resp)
    except Exception as e:
        logging.error(e)
 


#String-to-Bool
def str_to_bool(s):
    if s == 'true':
            return True
    elif s == 'false':
            return False
    elif s == 'True':
            return True
    elif s == 'False':
        return False



def sendIOTmessage (message):
    
    #Connection Settings
    deviceID = "fibarohome"
    iotHubAPIVer = "2018-04-01"
    iotHubRestURI = "https://vhomeiothub.azure-devices.net/devices/" + deviceID + "/messages/events?" + "api-version=" + iotHubAPIVer
    SASToken = 'SharedAccessSignature sr=vhomeiothub.azure-devices.net&sig=ckrtQT%2BbGkRP8BAr7MJ4rAHJncDR2xnVTWmgJQCjdX0%3D&se=1562707128&skn=iothubowner'

    Headers = {}
    Headers['Authorization'] = SASToken
    Headers['Content-Type'] = "application/json"

    idatetime =  datetime.datetime.now()
    body = {}
    body['datetime'] = str(idatetime)
    body['deviceClient'] = deviceID
    body['Message'] = message

    # Send Message
    try:
        resp = requests.post(iotHubRestURI, json=body, headers=Headers)
        #print(resp)
    except Exception as e:
        logging.error(e)
 
    




#String-to-Bool
def str_to_bool(s):
    if s == 'true':
            return True
    elif s == 'false':
            return False
    elif s == 'True':
            return True
    elif s == 'False':
        return False

while True:
    json_propertyvalues = requests.get("http://" + hcl_host + "/api/devices", auth=(hcl_user, hcl_password))
    p = json.loads(json_propertyvalues.text)
    l = len(p)

    client = InfluxDBClient(host, port, user, password, dbname,retries=3)
    timestamp = calendar.timegm(time.gmtime()) * 1000000000

   


    for i in range(0, l):
        if 'baseType' in p[i]: 

            if 'com.fibaro.weather' in p[i]['baseType']:
                #Weather Device properties
                try:
                    WeatherRoomId= str(p[i]['roomID'])
                    RoomW= requests.get("http://" + hcl_host + "/api/rooms/" + WeatherRoomId , auth=(hcl_user, hcl_password))
                    RoomResp = json.loads(RoomW.text)
                    RoomName= RoomResp['name']
                    WeatherDevEnabled= bool(p[i]['enabled'])

                    Humidity = float(p[i]['properties']['Humidity'])
                    Pressure = float(p[i]['properties']['Pressure'])
                    Temperature = float(p[i]['properties']['Temperature'])
                    Wind = float(p[i]['properties']['Wind'])

                    deviceid = p[i]['id']
                    devicename = p[i]['name']
                    json_body = [
                            {
                                "measurement": "homepi",
                                "tags": {
                                    "Device": deviceid,
                                    "Name": devicename,
                                    "Room" : RoomName
                            
                                },
                                "time": timestamp,
                                "fields": {
                                    "Humidity": Humidity,
                                    "Pressure" : Pressure,
                                    "Temperature" : Temperature,
                                    "Wind": Wind,
                                    "DeviceStatus" : WeatherDevEnabled
                                }
                            }
                        ]
                    client.write_points(json_body)
                except Exception as e:
                    logging.error(e)
                try:
                    imessage = [
                        {
                                "Device": deviceid,
                                "Name": devicename,
                                "Room" : RoomName,
                                "time": timestamp,   
                                "Humidity": Humidity,
                                "Pressure" : Pressure,
                                "Temperature" : Temperature,
                                "Wind": Wind,
                                "DeviceStatus" : WeatherDevEnabled
                            }
                        ]
                    sendIOTmessage(imessage)
                except Exception as e:
                     logging.error(e)


            elif 'com.fibaro.multilevelSwitch' in p[i]['baseType']:
                #Light Sensors
                try:
                    json_body = None
                    RoomName = None
                    LightsRoomID = str(p[i]['roomID'])
                    RoomW= requests.get("http://" + hcl_host + "/api/rooms/" + LightsRoomID, auth=(hcl_user, hcl_password))
                    RoomResp = json.loads(RoomW.text)
                    RoomName= RoomResp['name']
                    deviceid = p[i]['id']
                    deviceidS = str(p[i]['id'])
                    devicename = p[i]['name']
                    LightsDevEnabled= p[i]['enabled']
                    power = float(p[i]['properties']['power'])
                    energy = float(p[i]['properties']['energy'])
                    dimlevel = float(p[i]['properties']['value'])

                    #Get Consumption Energy
                    consumptionreq= requests.get("http://" + hcl_host + "/api/energy/now/now/summary-graph/devices/power/" + deviceidS, auth=(hcl_user, hcl_password))
                    consumptionres= json.loads(consumptionreq.text)
                    consumption = float(consumptionres[0][1])
            
                    #Get Consumption Money
                    consumptionreqmoney = requests.get("http://" + hcl_host + "/api/energy/now/now/summary-graph/devices/money/" + deviceidS, auth=(hcl_user, hcl_password))
                    consumptionresmoney= json.loads(consumptionreqmoney.text)
                    consumptionmoney = float(consumptionresmoney[0][1])
                    finalmoneyconsumed =  consumptionmoney / 1000 * 0.12

                    json_body = [
                            {
                                "measurement": "homepi",
                                "tags": {
                                    "Device": deviceid,
                                    "Name": devicename,
                                    "Room" : RoomName
                        
                                },
                                "time": timestamp,
                                "fields": {
                                    "DeviceStatus" : LightsDevEnabled,
                                    "PowerConsumed": power,
                                    "EnergyConsumed" : energy,
                                    "DimLevel" : dimlevel,
                                    "ActualEnergyConsumed" : consumption,
                                    "ActualMoneyConsumed" : consumptionmoney
                                }
                            }
                        ]
                    client.write_points(json_body)
                except Exception as e:
                    logging.error(e)
                try:
                    message = [
                        {
                            "Device": deviceid,
                            "Name": devicename,
                            "Room" : RoomName,
                            "time": timestamp,   
                            "PowerConsumed": power,
                            "EnergyConsumed" : energy,
                            "DimLevel" : dimlevel,
                            "ActualEnergyConsumed" : consumption,
                            "ActualMoneyConsumed" : consumptionmoney,
                            "DeviceStatus" : LightsDevEnabled
                        }
                   ]
                    sendIOTmessage(message)
                except Exception as e:
                    logging.error(e)

            elif 'com.fibaro.motionSensor' in p[i]['baseType']:
                #Motion Detector Sensors
                try:
                    json_body = None
                    RoomName = None
                    MotionRoomID = str(p[i]['roomID'])
                    RoomM= requests.get("http://" + hcl_host + "/api/rooms/" + MotionRoomID, auth=(hcl_user, hcl_password))
                    RoomResp = json.loads(RoomM.text)
                    RoomName= RoomResp['name']
                    deviceid = p[i]['id']
                    devicename = p[i]['name']
                    MotionDevEnabled= p[i]['enabled']
                    armed = p[i]['properties']['armed']
                    batterylevel = float(p[i]['properties']['batteryLevel'])
                    motiondetect = p[i]['properties']['value']
                    json_body = [
                        {
                            "measurement": "homepi",
                            "tags": {
                                "Device": deviceid,
                                "Name": devicename,
                                "Room" : RoomName
                        
                            },
                            "time": timestamp,
                            "fields": {
                                "DeviceStatus" : MotionDevEnabled,
                                "IsSensorArmed": str_to_bool(armed),
                                "BatteryLevel" : batterylevel,
                                "DimLevel" : dimlevel,
                                "MotionDetected" :str_to_bool(motiondetect)
                            }
                        }
                    ]
                    client.write_points(json_body)
                except Exception as e:
                    logging.error(e)
                try:
                    message = [
                        {
                            "Device": deviceid,
                            "Name": devicename,
                            "Room" : RoomName,
                            "time": timestamp,   
                            "IsSensorArmed": str_to_bool(armed),
                            "BatteryLevel" : batterylevel,
                            "DimLevel" : dimlevel,
                            "DeviceStatus" : MotionDevEnabled
                        }
                   ]
                    sendIOTmessage(message)
                except Exception as e:
                    logging.error(e)
            elif 'com.fibaro.lightSensor' in p[i]['type']:
                #Light Sensors
                try:
                    json_body = None
                    RoomName = None
                    LightSensRoomID = str(p[i]['roomID'])
                    RoomL= requests.get("http://" + hcl_host + "/api/rooms/" + LightSensRoomID, auth=(hcl_user, hcl_password))
                    RoomLResp = json.loads(RoomL.text)
                    RoomName= RoomLResp['name']
                    deviceid = p[i]['id']
                    devicename = p[i]['name']
                    LightsSensDevEnabled= p[i]['enabled']
                    lux= float(p[i]['properties']['value'])
                    json_body = [
                        {
                            "measurement": "homepi",
                            "tags": {
                                "Device": deviceid,
                                "Name": devicename,
                                "Room" : RoomName
                        
                            },
                            "time": timestamp,
                            "fields": {
                                "DeviceStatus" : LightsSensDevEnabled,
                                "luminance": lux
                            }
                        }
                    ]
                    client.write_points(json_body)
                except Exception as e:
                    logging.error(e)
                try:
                    message = [
                        {
                            "Device": deviceid,
                            "Name": devicename,
                            "Room" : RoomName,
                            "time": timestamp,   
                            "luminance": lux,
                            "DeviceStatus" : LightsSensDevEnabled
                        }
                   ]
                    sendIOTmessage(message)
                except Exception as e:
                    logging.error(e)
            elif 'com.fibaro.smokeSensor' in p[i]['type']:
                    #Smoke Detector Sensors
                try:
                    json_body = None
                    RoomName = None
                    SmokeSensRoomID = str(p[i]['roomID'])
                    RoomS= requests.get("http://" + hcl_host + "/api/rooms/" + SmokeSensRoomID, auth=(hcl_user, hcl_password))
                    RoomSResp = json.loads(RoomS.text)
                    RoomName= RoomSResp['name']
                    deviceid = p[i]['id']
                    devicename = p[i]['name']
                    SmokeSensDevEnabled= p[i]['enabled']
                    SmokeDetection= p[i]['properties']['value']
                    SmokeDetectBatteryLevel= float(p[i]['properties']['batteryLevel'])
                    json_body = [
                        {
                            "measurement": "homepi",
                            "tags": {
                                "Device": deviceid,
                                "Name": devicename,
                                "Room" : RoomName
                        
                            },
                            "time": timestamp,
                            "fields": {
                                "DeviceStatus" : SmokeSensDevEnabled,
                                "SmokeDetection": str_to_bool(SmokeDetection),
                                "BatteryLevel": SmokeDetectBatteryLevel
                            }
                        }
                    ]
                    client.write_points(json_body)
                except Exception as e:
                    logging.error(e)
                try:
                    message = [
                        {
                            "Device": deviceid,
                            "Name": devicename,
                            "Room" : RoomName,
                            "time": timestamp,   
                            "SmokeDetection": str_to_bool(SmokeDetection),
                            "BatteryLevel": SmokeDetectBatteryLevel,
                            "DeviceStatus" : SmokeSensDevEnabled
                        }
                   ]
                    sendIOTmessage(message)
                except Exception as e:
                    logging.error(e)
            elif 'com.fibaro.binarySwitch' in p[i]['type']:
                #Power Switch Sensors
                try:
                    json_body = None
                    RoomName = None
                    PowerSwitchRoomID = str(p[i]['roomID'])
                    RoomP= requests.get("http://" + hcl_host + "/api/rooms/" + PowerSwitchRoomID, auth=(hcl_user, hcl_password))
                    RoomPResp = json.loads(RoomP.text)
                    RoomName= RoomPResp['name']
                    deviceid = p[i]['id']
                    deviceidS = str(p[i]['id'])
                    devicename = p[i]['name']
                    spower= float(p[i]['properties']['power'])
                    PowerSDevEnabled= p[i]['enabled']
                    senergy= float(p[i]['properties']['energy'])
                    powerEnabled= p[i]['properties']['value']
                
                        #Get Consumption Energy
                    sconsumptionreq= requests.get("http://" + hcl_host + "/api/energy/now/now/summary-graph/devices/power/" + deviceidS, auth=(hcl_user, hcl_password))
                    sconsumptionres= json.loads(sconsumptionreq.text)
                    sconsumption = float(sconsumptionres[0][1])
            
                    #Get Consumption Money
                    sconsumptionreqmoney = requests.get("http://" + hcl_host + "/api/energy/now/now/summary-graph/devices/money/" + deviceidS, auth=(hcl_user, hcl_password))
                    sconsumptionresmoney= json.loads(sconsumptionreqmoney.text)
                    sconsumptionmoney = float(sconsumptionresmoney[0][1])
                    finalmoneyconsumed =  sconsumptionmoney / 1000 * 0.12
                
                    json_body = [
                        {
                            "measurement": "homepi",
                            "tags": {
                                "Device": deviceid,
                                "Name": devicename,
                                "Room" : RoomName
                        
                            },
                            "time": timestamp,
                                "fields": {
                                    "DeviceStatus" : PowerSDevEnabled,
                                    "PowerConsumed": spower,
                                    "EnergyConsumed" : senergy,
                                    "ActualEnergyConsumed" : sconsumption,
                                    "ActualMoneyConsumed" :finalmoneyconsumed,
                                    "PowerPlugIsOn": str_to_bool(powerEnabled)
                                }
                        
                        }
                    ]
                    client.write_points(json_body)
                except Exception as e:
                    logging.error(e)
                try:
                    message = [
                        {
                            "Device": deviceid,
                            "Name": devicename,
                            "Room" : RoomName,
                            "time": timestamp,   
                            "PowerConsumed": spower,
                            "EnergyConsumed" : senergy,
                            "ActualEnergyConsumed" : sconsumption,
                            "ActualMoneyConsumed" :finalmoneyconsumed,
                            "DeviceStatus" : PowerSDevEnabled
                        }
                    ]
                    sendIOTmessage(message)
                except Exception as e:
                    logging.error(e)

            elif 'com.fibaro.sensor' in p[i]['baseType']:
                #Voltage Sensors
                try:
                    json_body = None
                    RoomName = None
                    VoltageSensRoomID = str(p[i]['roomID'])
                    RoomV= requests.get("http://" + hcl_host + "/api/rooms/" + VoltageSensRoomID , auth=(hcl_user, hcl_password))
                    RoomVResp = json.loads(RoomV.text)
                    RoomName= RoomVResp['name']
                    deviceid = p[i]['id']
                    devicename = p[i]['name']
                    VDevEnabled= p[i]['enabled']
                    VValue= float(p[i]['properties']['value'])
                
                    json_body = [
                        {
                            "measurement": "homepi",
                            "tags": {
                                "Device": deviceid,
                                "Name": devicename,
                                "Room" : RoomName
                        
                            },
                            "time": timestamp,
                            "fields": {
                                "DeviceStatus" : VDevEnabled,
                                "VoltageValue": VValue
                            }
                        }
                    ]
                    client.write_points(json_body)
                except Exception as e:
                    logging.error(e)
                try:
                    message = [
                        {
                            "Device": deviceid,
                            "Name": devicename,
                            "Room" : RoomName,
                            "time": timestamp,   
                            "VoltageValue": VValue,
                            "DeviceStatus" : PowerSDevEnabled
                        }
                    ]
                    sendIOTmessage(message)
                except Exception as e:
                    logging.error(e)

            
            elif 'com.fibaro.doorWindowSensor' in p[i]['baseType']:
                #Voltage Sensors
                try:
                    json_body = None
                    RoomName = None
                    batterylevel=None
                    armed = None
                    value = None
                    DoorSensRoomID = str(p[i]['roomID'])
                    RoomD= requests.get("http://" + hcl_host + "/api/rooms/" + DoorSensRoomID, auth=(hcl_user, hcl_password))
                    RoomDResp = json.loads(RoomD.text)
                    RoomName= RoomDResp['name']
                    deviceid = p[i]['id']
                    devicename = p[i]['name']
                    DoorSensorEnabled= p[i]['enabled']
                    SensorValue= p[i]['properties']['value']
                    batterylevel = float(p[i]['properties']['batteryLevel'])
                    armed = p[i]['properties']['armed']
                    json_body = [
                    {
                        "measurement": "homepi",
                        "tags": {
                            "Device": deviceid,
                            "Name": devicename,
                            "Room" : RoomName
                        
                        },
                        "time": timestamp,
                        "fields": {
                            "DeviceStatus" : DoorSensorEnabled,
                            "IsDoorOpened": str_to_bool(SensorValue),
                            "BatteryLevel": batterylevel,
                            "IsSensorArmed" : str_to_bool(armed)

                        }
                    }
                ]
                    client.write_points(json_body)
                except Exception as e:
                    logging.error(e)
                try:
                    message = [
                        {
                            "Device": deviceid,
                            "Name": devicename,
                            "Room" : RoomName,
                            "time": timestamp,   
                            "IsDoorOpened": str_to_bool(SensorValue),
                            "BatteryLevel": batterylevel,
                            "IsSensorArmed" : str_to_bool(armed),
                            "DeviceStatus" : DoorSensorEnabled
                        }
                    ]
                    #message = json.dumps(imessage).encode('utf-8')
                    sendIOTmessage(message)
                except Exception as e:
                    logging.error(e)

            elif 'com.fibaro.temperatureSensor' in p[i]['type']:
                #Temperature Sensors
                try:
                    json_body = None
                    RoomName = None
                    TempSensRoomID = str(p[i]['roomID'])
                    RoomT= requests.get("http://" + hcl_host + "/api/rooms/" + TempSensRoomID, auth=(hcl_user, hcl_password))
                    RoomTResp = json.loads(RoomT.text)
                    RoomName= RoomTResp['name']
                    deviceid = p[i]['id']
                    devicename = p[i]['name']
                    TempSensDevEnabled= p[i]['enabled']
                    Temp= float(p[i]['properties']['value'])
                
                    json_body = [
                        {
                            "measurement": "homepi",
                            "tags": {
                                "Device": deviceid,
                                "Name": devicename,
                                "Room" : RoomName
                        
                            },
                            "time": timestamp,
                            "fields": {
                                "DeviceStatus" : TempSensDevEnabled,
                                "Temperature": Temp
                            }
                        }
                    ]
                    client.write_points(json_body)
                except Exception as e:
                    logging.error(e)
                try:
                    message = [
                        {
                            "Device": deviceid,
                            "Name": devicename,
                            "Room" : RoomName,
                            "time": timestamp,   
                            "Temperature": Temp,
                            "DeviceStatus" : TempSensDevEnabled
                        }
                    ]
                    sendIOTmessage(message)
                except Exception as e:
                    logging.error(e)
            elif 'com.fibaro.hvac' in p[i]['baseType']:
                #Temperature Sensors
                try:
                    json_body = None
                    RoomName = None
                    AirCSensRoomID = str(p[i]['roomID'])
                    RoomACR= requests.get("http://" + hcl_host + "/api/rooms/" + AirCSensRoomID, auth=(hcl_user, hcl_password))
                    RoomACResp = json.loads(RoomACR.text)
                    RoomName= RoomACResp['name']
                    deviceid = p[i]['id']
                    devicename = p[i]['name']
                    ACDevEnabled= p[i]['enabled']
                    value= float(p[i]['properties']['value'])
                    batterylevel= float(p[i]['properties']['batteryLevel'])
                
                    json_body = [
                        {
                            "measurement": "homepi",
                            "tags": {
                                "Device": deviceid,
                                "Name": devicename,
                                "Room" : RoomName
                        
                            },
                            "time": timestamp,
                            "fields": {
                                "DeviceStatus" : ACDevEnabled,
                                "Temperature": value,
                                "BatteryLevel": batterylevel
                            }
                        }
                    ]
                    client.write_points(json_body)
                except Exception as e:
                    logging.error(e)
                try:
                    message = [
                        {
                            "Device": deviceid,
                            "Name": devicename,
                            "Room" : RoomName,
                            "time": timestamp,   
                            "Temperature": value,
                            "BatteryLevel": batterylevel,
                            "DeviceStatus" : ACDevEnabled
                        }
                    ]
                    sendIOTmessage(message)
                except Exception as e:
                    logging.error(e)
    time.sleep(60)            
    json_propertyvalues = requests.get("http://" + hcl_host + "/api/devices", auth=(hcl_user, hcl_password))
    p = json.loads(json_propertyvalues.text)
    l = len(p)

    client = InfluxDBClient(host, port, user, password, dbname,retries=3)
    timestamp = calendar.timegm(time.gmtime()) * 1000000000

   


    for i in range(0, l):
        if 'baseType' in p[i]: 

            if 'com.fibaro.weather' in p[i]['baseType']:
                #Weather Device properties
                try:
                    WeatherRoomId= str(p[i]['roomID'])
                    RoomW= requests.get("http://" + hcl_host + "/api/rooms/" + WeatherRoomId , auth=(hcl_user, hcl_password))
                    RoomResp = json.loads(RoomW.text)
                    RoomName= RoomResp['name']
                    WeatherDevEnabled= bool(p[i]['enabled'])

                    Humidity = float(p[i]['properties']['Humidity'])
                    Pressure = float(p[i]['properties']['Pressure'])
                    Temperature = float(p[i]['properties']['Temperature'])
                    Wind = float(p[i]['properties']['Wind'])

                    deviceid = p[i]['id']
                    devicename = p[i]['name']
                    json_body = [
                            {
                                "measurement": "homepi",
                                "tags": {
                                    "Device": deviceid,
                                    "Name": devicename,
                                    "Room" : RoomName
                            
                                },
                                "time": timestamp,
                                "fields": {
                                    "Humidity": Humidity,
                                    "Pressure" : Pressure,
                                    "Temperature" : Temperature,
                                    "Wind": Wind,
                                    "DeviceStatus" : WeatherDevEnabled
                                }
                            }
                        ]
                    client.write_points(json_body)
                except Exception as e:
                    logging.error(e)
                try:
                    imessage = [
                        {
                                "Device": deviceid,
                                "Name": devicename,
                                "Room" : RoomName,
                                "time": timestamp,   
                                "Humidity": Humidity,
                                "Pressure" : Pressure,
                                "Temperature" : Temperature,
                                "Wind": Wind,
                                "DeviceStatus" : WeatherDevEnabled
                            }
                        ]
                    sendIOTmessage(imessage)
                except Exception as e:
                     logging.error(e)


            elif 'com.fibaro.multilevelSwitch' in p[i]['baseType']:
                #Light Sensors
                try:
                    json_body = None
                    RoomName = None
                    LightsRoomID = str(p[i]['roomID'])
                    RoomW= requests.get("http://" + hcl_host + "/api/rooms/" + LightsRoomID, auth=(hcl_user, hcl_password))
                    RoomResp = json.loads(RoomW.text)
                    RoomName= RoomResp['name']
                    deviceid = p[i]['id']
                    deviceidS = str(p[i]['id'])
                    devicename = p[i]['name']
                    LightsDevEnabled= p[i]['enabled']
                    power = float(p[i]['properties']['power'])
                    energy = float(p[i]['properties']['energy'])
                    dimlevel = float(p[i]['properties']['value'])

                    #Get Consumption Energy
                    consumptionreq= requests.get("http://" + hcl_host + "/api/energy/now/now/summary-graph/devices/power/" + deviceidS, auth=(hcl_user, hcl_password))
                    consumptionres= json.loads(consumptionreq.text)
                    consumption = float(consumptionres[0][1])
            
                    #Get Consumption Money
                    consumptionreqmoney = requests.get("http://" + hcl_host + "/api/energy/now/now/summary-graph/devices/money/" + deviceidS, auth=(hcl_user, hcl_password))
                    consumptionresmoney= json.loads(consumptionreqmoney.text)
                    consumptionmoney = float(consumptionresmoney[0][1])
                    finalmoneyconsumed =  consumptionmoney / 1000 * 0.12

                    json_body = [
                            {
                                "measurement": "homepi",
                                "tags": {
                                    "Device": deviceid,
                                    "Name": devicename,
                                    "Room" : RoomName
                        
                                },
                                "time": timestamp,
                                "fields": {
                                    "DeviceStatus" : LightsDevEnabled,
                                    "PowerConsumed": power,
                                    "EnergyConsumed" : energy,
                                    "DimLevel" : dimlevel,
                                    "ActualEnergyConsumed" : consumption,
                                    "ActualMoneyConsumed" : consumptionmoney
                                }
                            }
                        ]
                    client.write_points(json_body)
                except Exception as e:
                    logging.error(e)
                try:
                    message = [
                        {
                            "Device": deviceid,
                            "Name": devicename,
                            "Room" : RoomName,
                            "time": timestamp,   
                            "PowerConsumed": power,
                            "EnergyConsumed" : energy,
                            "DimLevel" : dimlevel,
                            "ActualEnergyConsumed" : consumption,
                            "ActualMoneyConsumed" : consumptionmoney,
                            "DeviceStatus" : LightsDevEnabled
                        }
                   ]
                    sendIOTmessage(message)
                except Exception as e:
                    logging.error(e)

            elif 'com.fibaro.motionSensor' in p[i]['baseType']:
                #Motion Detector Sensors
                try:
                    json_body = None
                    RoomName = None
                    MotionRoomID = str(p[i]['roomID'])
                    RoomM= requests.get("http://" + hcl_host + "/api/rooms/" + MotionRoomID, auth=(hcl_user, hcl_password))
                    RoomResp = json.loads(RoomM.text)
                    RoomName= RoomResp['name']
                    deviceid = p[i]['id']
                    devicename = p[i]['name']
                    MotionDevEnabled= p[i]['enabled']
                    armed = p[i]['properties']['armed']
                    batterylevel = float(p[i]['properties']['batteryLevel'])
                    motiondetect = p[i]['properties']['value']
                    json_body = [
                        {
                            "measurement": "homepi",
                            "tags": {
                                "Device": deviceid,
                                "Name": devicename,
                                "Room" : RoomName
                        
                            },
                            "time": timestamp,
                            "fields": {
                                "DeviceStatus" : MotionDevEnabled,
                                "IsSensorArmed": str_to_bool(armed),
                                "BatteryLevel" : batterylevel,
                                "DimLevel" : dimlevel,
                                "MotionDetected" :str_to_bool(motiondetect)
                            }
                        }
                    ]
                    client.write_points(json_body)
                except Exception as e:
                    logging.error(e)
                try:
                    message = [
                        {
                            "Device": deviceid,
                            "Name": devicename,
                            "Room" : RoomName,
                            "time": timestamp,   
                            "IsSensorArmed": str_to_bool(armed),
                            "BatteryLevel" : batterylevel,
                            "DimLevel" : dimlevel,
                            "DeviceStatus" : MotionDevEnabled
                        }
                   ]
                    sendIOTmessage(message)
                except Exception as e:
                    logging.error(e)
            elif 'com.fibaro.lightSensor' in p[i]['type']:
                #Light Sensors
                try:
                    json_body = None
                    RoomName = None
                    LightSensRoomID = str(p[i]['roomID'])
                    RoomL= requests.get("http://" + hcl_host + "/api/rooms/" + LightSensRoomID, auth=(hcl_user, hcl_password))
                    RoomLResp = json.loads(RoomL.text)
                    RoomName= RoomLResp['name']
                    deviceid = p[i]['id']
                    devicename = p[i]['name']
                    LightsSensDevEnabled= p[i]['enabled']
                    lux= float(p[i]['properties']['value'])
                    json_body = [
                        {
                            "measurement": "homepi",
                            "tags": {
                                "Device": deviceid,
                                "Name": devicename,
                                "Room" : RoomName
                        
                            },
                            "time": timestamp,
                            "fields": {
                                "DeviceStatus" : LightsSensDevEnabled,
                                "luminance": lux
                            }
                        }
                    ]
                    client.write_points(json_body)
                except Exception as e:
                    logging.error(e)
                try:
                    message = [
                        {
                            "Device": deviceid,
                            "Name": devicename,
                            "Room" : RoomName,
                            "time": timestamp,   
                            "luminance": lux,
                            "DeviceStatus" : LightsSensDevEnabled
                        }
                   ]
                    sendIOTmessage(message)
                except Exception as e:
                    logging.error(e)
            elif 'com.fibaro.smokeSensor' in p[i]['type']:
                    #Smoke Detector Sensors
                try:
                    json_body = None
                    RoomName = None
                    SmokeSensRoomID = str(p[i]['roomID'])
                    RoomS= requests.get("http://" + hcl_host + "/api/rooms/" + SmokeSensRoomID, auth=(hcl_user, hcl_password))
                    RoomSResp = json.loads(RoomS.text)
                    RoomName= RoomSResp['name']
                    deviceid = p[i]['id']
                    devicename = p[i]['name']
                    SmokeSensDevEnabled= p[i]['enabled']
                    SmokeDetection= p[i]['properties']['value']
                    SmokeDetectBatteryLevel= float(p[i]['properties']['batteryLevel'])
                    json_body = [
                        {
                            "measurement": "homepi",
                            "tags": {
                                "Device": deviceid,
                                "Name": devicename,
                                "Room" : RoomName
                        
                            },
                            "time": timestamp,
                            "fields": {
                                "DeviceStatus" : SmokeSensDevEnabled,
                                "SmokeDetection": str_to_bool(SmokeDetection),
                                "BatteryLevel": SmokeDetectBatteryLevel
                            }
                        }
                    ]
                    client.write_points(json_body)
                except Exception as e:
                    logging.error(e)
                try:
                    message = [
                        {
                            "Device": deviceid,
                            "Name": devicename,
                            "Room" : RoomName,
                            "time": timestamp,   
                            "SmokeDetection": str_to_bool(SmokeDetection),
                            "BatteryLevel": SmokeDetectBatteryLevel,
                            "DeviceStatus" : SmokeSensDevEnabled
                        }
                   ]
                    sendIOTmessage(message)
                except Exception as e:
                    logging.error(e)
            elif 'com.fibaro.binarySwitch' in p[i]['type']:
                #Power Switch Sensors
                try:
                    json_body = None
                    RoomName = None
                    PowerSwitchRoomID = str(p[i]['roomID'])
                    RoomP= requests.get("http://" + hcl_host + "/api/rooms/" + PowerSwitchRoomID, auth=(hcl_user, hcl_password))
                    RoomPResp = json.loads(RoomP.text)
                    RoomName= RoomPResp['name']
                    deviceid = p[i]['id']
                    deviceidS = str(p[i]['id'])
                    devicename = p[i]['name']
                    spower= float(p[i]['properties']['power'])
                    PowerSDevEnabled= p[i]['enabled']
                    senergy= float(p[i]['properties']['energy'])
                    powerEnabled= p[i]['properties']['value']
                
                        #Get Consumption Energy
                    sconsumptionreq= requests.get("http://" + hcl_host + "/api/energy/now/now/summary-graph/devices/power/" + deviceidS, auth=(hcl_user, hcl_password))
                    sconsumptionres= json.loads(sconsumptionreq.text)
                    sconsumption = float(sconsumptionres[0][1])
            
                    #Get Consumption Money
                    sconsumptionreqmoney = requests.get("http://" + hcl_host + "/api/energy/now/now/summary-graph/devices/money/" + deviceidS, auth=(hcl_user, hcl_password))
                    sconsumptionresmoney= json.loads(sconsumptionreqmoney.text)
                    sconsumptionmoney = float(sconsumptionresmoney[0][1])
                    finalmoneyconsumed =  sconsumptionmoney / 1000 * 0.12
                
                    json_body = [
                        {
                            "measurement": "homepi",
                            "tags": {
                                "Device": deviceid,
                                "Name": devicename,
                                "Room" : RoomName
                        
                            },
                            "time": timestamp,
                                "fields": {
                                    "DeviceStatus" : PowerSDevEnabled,
                                    "PowerConsumed": spower,
                                    "EnergyConsumed" : senergy,
                                    "ActualEnergyConsumed" : sconsumption,
                                    "ActualMoneyConsumed" :finalmoneyconsumed,
                                    "PowerPlugIsOn": str_to_bool(powerEnabled)
                                }
                        
                        }
                    ]
                    client.write_points(json_body)
                except Exception as e:
                    logging.error(e)
                try:
                    message = [
                        {
                            "Device": deviceid,
                            "Name": devicename,
                            "Room" : RoomName,
                            "time": timestamp,   
                            "PowerConsumed": spower,
                            "EnergyConsumed" : senergy,
                            "ActualEnergyConsumed" : sconsumption,
                            "ActualMoneyConsumed" :finalmoneyconsumed,
                            "DeviceStatus" : PowerSDevEnabled
                        }
                    ]
                    sendIOTmessage(message)
                except Exception as e:
                    logging.error(e)

            elif 'com.fibaro.sensor' in p[i]['baseType']:
                #Voltage Sensors
                try:
                    json_body = None
                    RoomName = None
                    VoltageSensRoomID = str(p[i]['roomID'])
                    RoomV= requests.get("http://" + hcl_host + "/api/rooms/" + VoltageSensRoomID , auth=(hcl_user, hcl_password))
                    RoomVResp = json.loads(RoomV.text)
                    RoomName= RoomVResp['name']
                    deviceid = p[i]['id']
                    devicename = p[i]['name']
                    VDevEnabled= p[i]['enabled']
                    VValue= float(p[i]['properties']['value'])
                
                    json_body = [
                        {
                            "measurement": "homepi",
                            "tags": {
                                "Device": deviceid,
                                "Name": devicename,
                                "Room" : RoomName
                        
                            },
                            "time": timestamp,
                            "fields": {
                                "DeviceStatus" : VDevEnabled,
                                "VoltageValue": VValue
                            }
                        }
                    ]
                    client.write_points(json_body)
                except Exception as e:
                    logging.error(e)
                try:
                    message = [
                        {
                            "Device": deviceid,
                            "Name": devicename,
                            "Room" : RoomName,
                            "time": timestamp,   
                            "VoltageValue": VValue,
                            "DeviceStatus" : PowerSDevEnabled
                        }
                    ]
                    sendIOTmessage(message)
                except Exception as e:
                    logging.error(e)

            
            elif 'com.fibaro.doorWindowSensor' in p[i]['baseType']:
                #Voltage Sensors
                try:
                    json_body = None
                    RoomName = None
                    batterylevel=None
                    armed = None
                    value = None
                    DoorSensRoomID = str(p[i]['roomID'])
                    RoomD= requests.get("http://" + hcl_host + "/api/rooms/" + DoorSensRoomID, auth=(hcl_user, hcl_password))
                    RoomDResp = json.loads(RoomD.text)
                    RoomName= RoomDResp['name']
                    deviceid = p[i]['id']
                    devicename = p[i]['name']
                    DoorSensorEnabled= p[i]['enabled']
                    SensorValue= p[i]['properties']['value']
                    batterylevel = float(p[i]['properties']['batteryLevel'])
                    armed = p[i]['properties']['armed']
                    json_body = [
                    {
                        "measurement": "homepi",
                        "tags": {
                            "Device": deviceid,
                            "Name": devicename,
                            "Room" : RoomName
                        
                        },
                        "time": timestamp,
                        "fields": {
                            "DeviceStatus" : DoorSensorEnabled,
                            "IsDoorOpened": str_to_bool(SensorValue),
                            "BatteryLevel": batterylevel,
                            "IsSensorArmed" : str_to_bool(armed)

                        }
                    }
                ]
                    client.write_points(json_body)
                except Exception as e:
                    logging.error(e)
                try:
                    message = [
                        {
                            "Device": deviceid,
                            "Name": devicename,
                            "Room" : RoomName,
                            "time": timestamp,   
                            "IsDoorOpened": str_to_bool(SensorValue),
                            "BatteryLevel": batterylevel,
                            "IsSensorArmed" : str_to_bool(armed),
                            "DeviceStatus" : DoorSensorEnabled
                        }
                    ]
                    #message = json.dumps(imessage).encode('utf-8')
                    sendIOTmessage(message)
                except Exception as e:
                    logging.error(e)

            elif 'com.fibaro.temperatureSensor' in p[i]['type']:
                #Temperature Sensors
                try:
                    json_body = None
                    RoomName = None
                    TempSensRoomID = str(p[i]['roomID'])
                    RoomT= requests.get("http://" + hcl_host + "/api/rooms/" + TempSensRoomID, auth=(hcl_user, hcl_password))
                    RoomTResp = json.loads(RoomT.text)
                    RoomName= RoomTResp['name']
                    deviceid = p[i]['id']
                    devicename = p[i]['name']
                    TempSensDevEnabled= p[i]['enabled']
                    Temp= float(p[i]['properties']['value'])
                
                    json_body = [
                        {
                            "measurement": "homepi",
                            "tags": {
                                "Device": deviceid,
                                "Name": devicename,
                                "Room" : RoomName
                        
                            },
                            "time": timestamp,
                            "fields": {
                                "DeviceStatus" : TempSensDevEnabled,
                                "Temperature": Temp
                            }
                        }
                    ]
                    client.write_points(json_body)
                except Exception as e:
                    logging.error(e)
                try:
                    message = [
                        {
                            "Device": deviceid,
                            "Name": devicename,
                            "Room" : RoomName,
                            "time": timestamp,   
                            "Temperature": Temp,
                            "DeviceStatus" : TempSensDevEnabled
                        }
                    ]
                    sendIOTmessage(message)
                except Exception as e:
                    logging.error(e)
            elif 'com.fibaro.hvac' in p[i]['baseType']:
                #Temperature Sensors
                try:
                    json_body = None
                    RoomName = None
                    AirCSensRoomID = str(p[i]['roomID'])
                    RoomACR= requests.get("http://" + hcl_host + "/api/rooms/" + AirCSensRoomID, auth=(hcl_user, hcl_password))
                    RoomACResp = json.loads(RoomACR.text)
                    RoomName= RoomACResp['name']
                    deviceid = p[i]['id']
                    devicename = p[i]['name']
                    ACDevEnabled= p[i]['enabled']
                    value= float(p[i]['properties']['value'])
                    batterylevel= float(p[i]['properties']['batteryLevel'])
                
                    json_body = [
                        {
                            "measurement": "homepi",
                            "tags": {
                                "Device": deviceid,
                                "Name": devicename,
                                "Room" : RoomName
                        
                            },
                            "time": timestamp,
                            "fields": {
                                "DeviceStatus" : ACDevEnabled,
                                "Temperature": value,
                                "BatteryLevel": batterylevel
                            }
                        }
                    ]
                    client.write_points(json_body)
                except Exception as e:
                    logging.error(e)
                try:
                    message = [
                        {
                            "Device": deviceid,
                            "Name": devicename,
                            "Room" : RoomName,
                            "time": timestamp,   
                            "Temperature": value,
                            "BatteryLevel": batterylevel,
                            "DeviceStatus" : ACDevEnabled
                        }
                    ]
                    sendIOTmessage(message)
                except Exception as e:
                    logging.error(e)
    time.sleep(60)    
    json_propertyvalues = requests.get("http://" + hcl_host + "/api/devices", auth=(hcl_user, hcl_password))
    p = json.loads(json_propertyvalues.text)
    l = len(p)

    client = InfluxDBClient(host, port, user, password, dbname,retries=3)
    timestamp = calendar.timegm(time.gmtime()) * 1000000000

   


    for i in range(0, l):
        if 'baseType' in p[i]: 

            if 'com.fibaro.weather' in p[i]['baseType']:
                #Weather Device properties
                try:
                    WeatherRoomId= str(p[i]['roomID'])
                    RoomW= requests.get("http://" + hcl_host + "/api/rooms/" + WeatherRoomId , auth=(hcl_user, hcl_password))
                    RoomResp = json.loads(RoomW.text)
                    RoomName= RoomResp['name']
                    WeatherDevEnabled= bool(p[i]['enabled'])

                    Humidity = float(p[i]['properties']['Humidity'])
                    Pressure = float(p[i]['properties']['Pressure'])
                    Temperature = float(p[i]['properties']['Temperature'])
                    Wind = float(p[i]['properties']['Wind'])

                    deviceid = p[i]['id']
                    devicename = p[i]['name']
                    json_body = [
                            {
                                "measurement": "homepi",
                                "tags": {
                                    "Device": deviceid,
                                    "Name": devicename,
                                    "Room" : RoomName
                            
                                },
                                "time": timestamp,
                                "fields": {
                                    "Humidity": Humidity,
                                    "Pressure" : Pressure,
                                    "Temperature" : Temperature,
                                    "Wind": Wind,
                                    "DeviceStatus" : WeatherDevEnabled
                                }
                            }
                        ]
                    client.write_points(json_body)
                except Exception as e:
                    logging.exception("message")
                    logging.error(e)
                try:
                    imessage = [
                        {
                                "Device": deviceid,
                                "Name": devicename,
                                "Room" : RoomName,
                                "time": timestamp,   
                                "Humidity": Humidity,
                                "Pressure" : Pressure,
                                "Temperature" : Temperature,
                                "Wind": Wind,
                                "DeviceStatus" : WeatherDevEnabled
                            }
                        ]
                    sendIOTmessage(imessage)
                except Exception as e:
                     logging.error(e)


            elif 'com.fibaro.multilevelSwitch' in p[i]['baseType']:
                #Light Sensors
                try:
                    json_body = None
                    RoomName = None
                    LightsRoomID = str(p[i]['roomID'])
                    RoomW= requests.get("http://" + hcl_host + "/api/rooms/" + LightsRoomID, auth=(hcl_user, hcl_password))
                    RoomResp = json.loads(RoomW.text)
                    RoomName= RoomResp['name']
                    deviceid = p[i]['id']
                    deviceidS = str(p[i]['id'])
                    devicename = p[i]['name']
                    LightsDevEnabled= p[i]['enabled']
                    power = float(p[i]['properties']['power'])
                    energy = float(p[i]['properties']['energy'])
                    dimlevel = float(p[i]['properties']['value'])

                    #Get Consumption Energy
                    consumptionreq= requests.get("http://" + hcl_host + "/api/energy/now/now/summary-graph/devices/power/" + deviceidS, auth=(hcl_user, hcl_password))
                    consumptionres= json.loads(consumptionreq.text)
                    consumption = float(consumptionres[0][1])
            
                    #Get Consumption Money
                    consumptionreqmoney = requests.get("http://" + hcl_host + "/api/energy/now/now/summary-graph/devices/money/" + deviceidS, auth=(hcl_user, hcl_password))
                    consumptionresmoney= json.loads(consumptionreqmoney.text)
                    consumptionmoney = float(consumptionresmoney[0][1])
                    finalmoneyconsumed =  consumptionmoney / 1000 * 0.12

                    json_body = [
                            {
                                "measurement": "homepi",
                                "tags": {
                                    "Device": deviceid,
                                    "Name": devicename,
                                    "Room" : RoomName
                        
                                },
                                "time": timestamp,
                                "fields": {
                                    "DeviceStatus" : LightsDevEnabled,
                                    "PowerConsumed": power,
                                    "EnergyConsumed" : energy,
                                    "DimLevel" : dimlevel,
                                    "ActualEnergyConsumed" : consumption,
                                    "ActualMoneyConsumed" : consumptionmoney
                                }
                            }
                        ]
                    client.write_points(json_body)
                except Exception as e:
                    logging.exception("message")
                    logging.error(e)
                try:
                    message = [
                        {
                            "Device": deviceid,
                            "Name": devicename,
                            "Room" : RoomName,
                            "time": timestamp,   
                            "PowerConsumed": power,
                            "EnergyConsumed" : energy,
                            "DimLevel" : dimlevel,
                            "ActualEnergyConsumed" : consumption,
                            "ActualMoneyConsumed" : consumptionmoney,
                            "DeviceStatus" : LightsDevEnabled
                        }
                   ]
                    sendIOTmessage(message)
                except Exception as e:
                    logging.error(e)

            elif 'com.fibaro.motionSensor' in p[i]['baseType']:
                #Motion Detector Sensors
                try:
                    json_body = None
                    RoomName = None
                    MotionRoomID = str(p[i]['roomID'])
                    RoomM= requests.get("http://" + hcl_host + "/api/rooms/" + MotionRoomID, auth=(hcl_user, hcl_password))
                    RoomResp = json.loads(RoomM.text)
                    RoomName= RoomResp['name']
                    deviceid = p[i]['id']
                    devicename = p[i]['name']
                    MotionDevEnabled= p[i]['enabled']
                    armed = p[i]['properties']['armed']
                    batterylevel = float(p[i]['properties']['batteryLevel'])
                    motiondetect = p[i]['properties']['value']
                    json_body = [
                        {
                            "measurement": "homepi",
                            "tags": {
                                "Device": deviceid,
                                "Name": devicename,
                                "Room" : RoomName
                        
                            },
                            "time": timestamp,
                            "fields": {
                                "DeviceStatus" : MotionDevEnabled,
                                "IsSensorArmed": str_to_bool(armed),
                                "BatteryLevel" : batterylevel,
                                "DimLevel" : dimlevel,
                                "MotionDetected" :str_to_bool(motiondetect)
                            }
                        }
                    ]
                    client.write_points(json_body)
                except Exception as e:
                    logging.exception("message")
                    logging.error(e)
                try:
                    message = [
                        {
                            "Device": deviceid,
                            "Name": devicename,
                            "Room" : RoomName,
                            "time": timestamp,   
                            "IsSensorArmed": str_to_bool(armed),
                            "BatteryLevel" : batterylevel,
                            "DimLevel" : dimlevel,
                            "DeviceStatus" : MotionDevEnabled
                        }
                   ]
                    #message = json.dumps(imessage).encode('utf-8')
                    sendIOTmessage(message)
                except Exception as e:
                    logging.error(e)
            elif 'com.fibaro.lightSensor' in p[i]['type']:
                #Light Sensors
                try:
                    json_body = None
                    RoomName = None
                    LightSensRoomID = str(p[i]['roomID'])
                    RoomL= requests.get("http://" + hcl_host + "/api/rooms/" + LightSensRoomID, auth=(hcl_user, hcl_password))
                    RoomLResp = json.loads(RoomL.text)
                    RoomName= RoomLResp['name']
                    deviceid = p[i]['id']
                    devicename = p[i]['name']
                    LightsSensDevEnabled= p[i]['enabled']
                    lux= float(p[i]['properties']['value'])
                    json_body = [
                        {
                            "measurement": "homepi",
                            "tags": {
                                "Device": deviceid,
                                "Name": devicename,
                                "Room" : RoomName
                        
                            },
                            "time": timestamp,
                            "fields": {
                                "DeviceStatus" : LightsSensDevEnabled,
                                "luminance": lux
                            }
                        }
                    ]
                    client.write_points(json_body)
                except Exception as e:
                    logging.exception("message")
                    logging.error(e)
                try:
                    message = [
                        {
                            "Device": deviceid,
                            "Name": devicename,
                            "Room" : RoomName,
                            "time": timestamp,   
                            "luminance": lux,
                            "DeviceStatus" : LightsSensDevEnabled
                        }
                   ]
                    #message = json.dumps(imessage).encode('utf-8')
                    sendIOTmessage(message)
                except Exception as e:
                    logging.error(e)
            elif 'com.fibaro.smokeSensor' in p[i]['type']:
                    #Smoke Detector Sensors
                try:
                    json_body = None
                    RoomName = None
                    SmokeSensRoomID = str(p[i]['roomID'])
                    RoomS= requests.get("http://" + hcl_host + "/api/rooms/" + SmokeSensRoomID, auth=(hcl_user, hcl_password))
                    RoomSResp = json.loads(RoomS.text)
                    RoomName= RoomSResp['name']
                    deviceid = p[i]['id']
                    devicename = p[i]['name']
                    SmokeSensDevEnabled= p[i]['enabled']
                    SmokeDetection= p[i]['properties']['value']
                    SmokeDetectBatteryLevel= float(p[i]['properties']['batteryLevel'])
                    json_body = [
                        {
                            "measurement": "homepi",
                            "tags": {
                                "Device": deviceid,
                                "Name": devicename,
                                "Room" : RoomName
                        
                            },
                            "time": timestamp,
                            "fields": {
                                "DeviceStatus" : SmokeSensDevEnabled,
                                "SmokeDetection": str_to_bool(SmokeDetection),
                                "BatteryLevel": SmokeDetectBatteryLevel
                            }
                        }
                    ]
                    client.write_points(json_body)
                except Exception as e:
                    logging.exception("message")
                    logging.error(e)
                try:
                    message = [
                        {
                            "Device": deviceid,
                            "Name": devicename,
                            "Room" : RoomName,
                            "time": timestamp,   
                            "SmokeDetection": str_to_bool(SmokeDetection),
                            "BatteryLevel": SmokeDetectBatteryLevel,
                            "DeviceStatus" : SmokeSensDevEnabled
                        }
                   ]
                    #message = json.dumps(imessage).encode('utf-8')
                    sendIOTmessage(message)
                except Exception as e:
                    logging.error(e)
            elif 'com.fibaro.binarySwitch' in p[i]['type']:
                #Power Switch Sensors
                try:
                    json_body = None
                    RoomName = None
                    PowerSwitchRoomID = str(p[i]['roomID'])
                    RoomP= requests.get("http://" + hcl_host + "/api/rooms/" + PowerSwitchRoomID, auth=(hcl_user, hcl_password))
                    RoomPResp = json.loads(RoomP.text)
                    RoomName= RoomPResp['name']
                    deviceid = p[i]['id']
                    deviceidS = str(p[i]['id'])
                    devicename = p[i]['name']
                    spower= float(p[i]['properties']['power'])
                    PowerSDevEnabled= p[i]['enabled']
                    senergy= float(p[i]['properties']['energy'])
                    powerEnabled= p[i]['properties']['value']
                
                        #Get Consumption Energy
                    sconsumptionreq= requests.get("http://" + hcl_host + "/api/energy/now/now/summary-graph/devices/power/" + deviceidS, auth=(hcl_user, hcl_password))
                    sconsumptionres= json.loads(sconsumptionreq.text)
                    sconsumption = float(sconsumptionres[0][1])
            
                    #Get Consumption Money
                    sconsumptionreqmoney = requests.get("http://" + hcl_host + "/api/energy/now/now/summary-graph/devices/money/" + deviceidS, auth=(hcl_user, hcl_password))
                    sconsumptionresmoney= json.loads(sconsumptionreqmoney.text)
                    sconsumptionmoney = float(sconsumptionresmoney[0][1])
                    finalmoneyconsumed =  sconsumptionmoney / 1000 * 0.12
                
                    json_body = [
                        {
                            "measurement": "homepi",
                            "tags": {
                                "Device": deviceid,
                                "Name": devicename,
                                "Room" : RoomName
                        
                            },
                            "time": timestamp,
                                "fields": {
                                    "DeviceStatus" : PowerSDevEnabled,
                                    "PowerConsumed": spower,
                                    "EnergyConsumed" : senergy,
                                    "ActualEnergyConsumed" : sconsumption,
                                    "ActualMoneyConsumed" :finalmoneyconsumed,
                                    "PowerPlugIsOn": str_to_bool(powerEnabled)
                                }
                        
                        }
                    ]
                    client.write_points(json_body)
                except Exception as e:
                    logging.exception("message")
                    logging.error(e)
                try:
                    message = [
                        {
                            "Device": deviceid,
                            "Name": devicename,
                            "Room" : RoomName,
                            "time": timestamp,   
                            "PowerConsumed": spower,
                            "EnergyConsumed" : senergy,
                            "ActualEnergyConsumed" : sconsumption,
                            "ActualMoneyConsumed" :finalmoneyconsumed,
                            "DeviceStatus" : PowerSDevEnabled
                        }
                    ]
                    #message = json.dumps(imessage).encode('utf-8')
                    sendIOTmessage(message)
                except Exception as e:
                    logging.error(e)

            elif 'com.fibaro.sensor' in p[i]['baseType']:
                #Voltage Sensors
                try:
                    json_body = None
                    RoomName = None
                    VoltageSensRoomID = str(p[i]['roomID'])
                    RoomV= requests.get("http://" + hcl_host + "/api/rooms/" + VoltageSensRoomID , auth=(hcl_user, hcl_password))
                    RoomVResp = json.loads(RoomV.text)
                    RoomName= RoomVResp['name']
                    deviceid = p[i]['id']
                    devicename = p[i]['name']
                    VDevEnabled= p[i]['enabled']
                    VValue= float(p[i]['properties']['value'])
                
                    json_body = [
                        {
                            "measurement": "homepi",
                            "tags": {
                                "Device": deviceid,
                                "Name": devicename,
                                "Room" : RoomName
                        
                            },
                            "time": timestamp,
                            "fields": {
                                "DeviceStatus" : VDevEnabled,
                                "VoltageValue": VValue
                            }
                        }
                    ]
                    client.write_points(json_body)
                except Exception as e:
                    logging.exception("message")
                    logging.error(e)
                try:
                    message = [
                        {
                            "Device": deviceid,
                            "Name": devicename,
                            "Room" : RoomName,
                            "time": timestamp,   
                            "VoltageValue": VValue,
                            "DeviceStatus" : PowerSDevEnabled
                        }
                    ]
                    #message = json.dumps(imessage).encode('utf-8')
                    sendIOTmessage(message)
                except Exception as e:
                    logging.error(e)

            
            elif 'com.fibaro.doorWindowSensor' in p[i]['baseType']:
                #Voltage Sensors
                try:
                    json_body = None
                    RoomName = None
                    batterylevel=None
                    armed = None
                    value = None
                    DoorSensRoomID = str(p[i]['roomID'])
                    RoomD= requests.get("http://" + hcl_host + "/api/rooms/" + DoorSensRoomID, auth=(hcl_user, hcl_password))
                    RoomDResp = json.loads(RoomD.text)
                    RoomName= RoomDResp['name']
                    deviceid = p[i]['id']
                    devicename = p[i]['name']
                    DoorSensorEnabled= p[i]['enabled']
                    SensorValue= p[i]['properties']['value']
                    batterylevel = float(p[i]['properties']['batteryLevel'])
                    armed = p[i]['properties']['armed']
                    json_body = [
                    {
                        "measurement": "homepi",
                        "tags": {
                            "Device": deviceid,
                            "Name": devicename,
                            "Room" : RoomName
                        
                        },
                        "time": timestamp,
                        "fields": {
                            "DeviceStatus" : DoorSensorEnabled,
                            "IsDoorOpened": str_to_bool(SensorValue),
                            "BatteryLevel": batterylevel,
                            "IsSensorArmed" : str_to_bool(armed)

                        }
                    }
                ]
                    client.write_points(json_body)
                except Exception as e:
                    logging.exception("message")
                    logging.error(e)
                try:
                    message = [
                        {
                            "Device": deviceid,
                            "Name": devicename,
                            "Room" : RoomName,
                            "time": timestamp,   
                            "IsDoorOpened": str_to_bool(SensorValue),
                            "BatteryLevel": batterylevel,
                            "IsSensorArmed" : str_to_bool(armed),
                            "DeviceStatus" : DoorSensorEnabled
                        }
                    ]
                    #message = json.dumps(imessage).encode('utf-8')
                    sendIOTmessage(message)
                except Exception as e:
                    logging.error(e)

            elif 'com.fibaro.temperatureSensor' in p[i]['type']:
                #Temperature Sensors
                try:
                    json_body = None
                    RoomName = None
                    TempSensRoomID = str(p[i]['roomID'])
                    RoomT= requests.get("http://" + hcl_host + "/api/rooms/" + TempSensRoomID, auth=(hcl_user, hcl_password))
                    RoomTResp = json.loads(RoomT.text)
                    RoomName= RoomTResp['name']
                    deviceid = p[i]['id']
                    devicename = p[i]['name']
                    TempSensDevEnabled= p[i]['enabled']
                    Temp= float(p[i]['properties']['value'])
                
                    json_body = [
                        {
                            "measurement": "homepi",
                            "tags": {
                                "Device": deviceid,
                                "Name": devicename,
                                "Room" : RoomName
                        
                            },
                            "time": timestamp,
                            "fields": {
                                "DeviceStatus" : TempSensDevEnabled,
                                "Temperature": Temp
                            }
                        }
                    ]
                    client.write_points(json_body)
                except Exception as e:
                    logging.exception("message")
                    logging.error(e)
                try:
                    message = [
                        {
                            "Device": deviceid,
                            "Name": devicename,
                            "Room" : RoomName,
                            "time": timestamp,   
                            "Temperature": Temp,
                            "DeviceStatus" : TempSensDevEnabled
                        }
                    ]
                    #message = json.dumps(imessage).encode('utf-8')
                    sendIOTmessage(message)
                except Exception as e:
                    logging.error(e)
            elif 'com.fibaro.hvac' in p[i]['baseType']:
                #Temperature Sensors
                try:
                    json_body = None
                    RoomName = None
                    AirCSensRoomID = str(p[i]['roomID'])
                    RoomACR= requests.get("http://" + hcl_host + "/api/rooms/" + AirCSensRoomID, auth=(hcl_user, hcl_password))
                    RoomACResp = json.loads(RoomACR.text)
                    RoomName= RoomACResp['name']
                    deviceid = p[i]['id']
                    devicename = p[i]['name']
                    ACDevEnabled= p[i]['enabled']
                    value= float(p[i]['properties']['value'])
                    batterylevel= float(p[i]['properties']['batteryLevel'])
                
                    json_body = [
                        {
                            "measurement": "homepi",
                            "tags": {
                                "Device": deviceid,
                                "Name": devicename,
                                "Room" : RoomName
                        
                            },
                            "time": timestamp,
                            "fields": {
                                "DeviceStatus" : ACDevEnabled,
                                "Temperature": value,
                                "BatteryLevel": batterylevel
                            }
                        }
                    ]
                    client.write_points(json_body)
                except Exception as e:
                    logging.exception("message")
                    logging.error(e)
                try:
                    message = [
                        {
                            "Device": deviceid,
                            "Name": devicename,
                            "Room" : RoomName,
                            "time": timestamp,   
                            "Temperature": value,
                            "BatteryLevel": batterylevel,
                            "DeviceStatus" : ACDevEnabled
                        }
                    ]
                    #message = json.dumps(imessage).encode('utf-8')
                    sendIOTmessage(message)
                except Exception as e:
                    logging.error(e)
    time.sleep(60)  
    json_propertyvalues = requests.get("http://" + hcl_host + "/api/devices", auth=(hcl_user, hcl_password))
    p = json.loads(json_propertyvalues.text)
    l = len(p)

    client = InfluxDBClient(host, port, user, password, dbname,retries=3)
    timestamp = calendar.timegm(time.gmtime()) * 1000000000

   


    for i in range(0, l):
        if 'baseType' in p[i]: 

            if 'com.fibaro.weather' in p[i]['baseType']:
                #Weather Device properties
                try:
                    WeatherRoomId= str(p[i]['roomID'])
                    RoomW= requests.get("http://" + hcl_host + "/api/rooms/" + WeatherRoomId , auth=(hcl_user, hcl_password))
                    RoomResp = json.loads(RoomW.text)
                    RoomName= RoomResp['name']
                    WeatherDevEnabled= bool(p[i]['enabled'])

                    Humidity = float(p[i]['properties']['Humidity'])
                    Pressure = float(p[i]['properties']['Pressure'])
                    Temperature = float(p[i]['properties']['Temperature'])
                    Wind = float(p[i]['properties']['Wind'])

                    deviceid = p[i]['id']
                    devicename = p[i]['name']
                    json_body = [
                            {
                                "measurement": "homepi",
                                "tags": {
                                    "Device": deviceid,
                                    "Name": devicename,
                                    "Room" : RoomName
                            
                                },
                                "time": timestamp,
                                "fields": {
                                    "Humidity": Humidity,
                                    "Pressure" : Pressure,
                                    "Temperature" : Temperature,
                                    "Wind": Wind,
                                    "DeviceStatus" : WeatherDevEnabled
                                }
                            }
                        ]
                    client.write_points(json_body)
                except Exception as e:
                    logging.exception("message")
                    logging.error(e)
            elif 'com.fibaro.multilevelSwitch' in p[i]['baseType']:
                #Light Sensors
                try:
                    json_body = None
                    RoomName = None
                    LightsRoomID = str(p[i]['roomID'])
                    RoomW= requests.get("http://" + hcl_host + "/api/rooms/" + LightsRoomID, auth=(hcl_user, hcl_password))
                    RoomResp = json.loads(RoomW.text)
                    RoomName= RoomResp['name']
                    deviceid = p[i]['id']
                    deviceidS = str(p[i]['id'])
                    devicename = p[i]['name']
                    LightsDevEnabled= p[i]['enabled']
                    power = float(p[i]['properties']['power'])
                    energy = float(p[i]['properties']['energy'])
                    dimlevel = float(p[i]['properties']['value'])

                    #Get Consumption Energy
                    consumptionreq= requests.get("http://" + hcl_host + "/api/energy/now/now/summary-graph/devices/power/" + deviceidS, auth=(hcl_user, hcl_password))
                    consumptionres= json.loads(consumptionreq.text)
                    consumption = float(consumptionres[0][1])
            
                    #Get Consumption Money
                    consumptionreqmoney = requests.get("http://" + hcl_host + "/api/energy/now/now/summary-graph/devices/money/" + deviceidS, auth=(hcl_user, hcl_password))
                    consumptionresmoney= json.loads(consumptionreqmoney.text)
                    consumptionmoney = float(consumptionresmoney[0][1])
                    finalmoneyconsumed =  consumptionmoney / 1000 * 0.12

                    json_body = [
                            {
                                "measurement": "homepi",
                                "tags": {
                                    "Device": deviceid,
                                    "Name": devicename,
                                    "Room" : RoomName
                        
                                },
                                "time": timestamp,
                                "fields": {
                                    "DeviceStatus" : LightsDevEnabled,
                                    "PowerConsumed": power,
                                    "EnergyConsumed" : energy,
                                    "DimLevel" : dimlevel,
                                    "ActualEnergyConsumed" : consumption,
                                    "ActualMoneyConsumed" : consumptionmoney
                                }
                            }
                        ]
                    client.write_points(json_body)
                except Exception as e:
                    logging.exception("message")
                    logging.error(e)

            elif 'com.fibaro.motionSensor' in p[i]['baseType']:
                #Motion Detector Sensors
                try:
                    json_body = None
                    RoomName = None
                    MotionRoomID = str(p[i]['roomID'])
                    RoomM= requests.get("http://" + hcl_host + "/api/rooms/" + MotionRoomID, auth=(hcl_user, hcl_password))
                    RoomResp = json.loads(RoomM.text)
                    RoomName= RoomResp['name']
                    deviceid = p[i]['id']
                    devicename = p[i]['name']
                    MotionDevEnabled= p[i]['enabled']
                    armed = p[i]['properties']['armed']
                    batterylevel = float(p[i]['properties']['batteryLevel'])
                    motiondetect = p[i]['properties']['value']
                    json_body = [
                        {
                            "measurement": "homepi",
                            "tags": {
                                "Device": deviceid,
                                "Name": devicename,
                                "Room" : RoomName
                        
                            },
                            "time": timestamp,
                            "fields": {
                                "DeviceStatus" : MotionDevEnabled,
                                "IsSensorArmed": str_to_bool(armed),
                                "BatteryLevel" : batterylevel,
                                "DimLevel" : dimlevel,
                                "MotionDetected" :str_to_bool(motiondetect)
                            }
                        }
                    ]
                    client.write_points(json_body)
                except Exception as e:
                    logging.exception("message")
                    logging.error(e)
            elif 'com.fibaro.lightSensor' in p[i]['type']:
                #Light Sensors
                try:
                    json_body = None
                    RoomName = None
                    LightSensRoomID = str(p[i]['roomID'])
                    RoomL= requests.get("http://" + hcl_host + "/api/rooms/" + LightSensRoomID, auth=(hcl_user, hcl_password))
                    RoomLResp = json.loads(RoomL.text)
                    RoomName= RoomLResp['name']
                    deviceid = p[i]['id']
                    devicename = p[i]['name']
                    LightsSensDevEnabled= p[i]['enabled']
                    lux= float(p[i]['properties']['value'])
                    json_body = [
                        {
                            "measurement": "homepi",
                            "tags": {
                                "Device": deviceid,
                                "Name": devicename,
                                "Room" : RoomName
                        
                            },
                            "time": timestamp,
                            "fields": {
                                "DeviceStatus" : LightsSensDevEnabled,
                                "luminance": lux
                            }
                        }
                    ]
                    client.write_points(json_body)
                except Exception as e:
                    logging.exception("message")
                    logging.error(e)
            elif 'com.fibaro.smokeSensor' in p[i]['type']:
                    #Smoke Detector Sensors
                try:
                    json_body = None
                    RoomName = None
                    SmokeSensRoomID = str(p[i]['roomID'])
                    RoomS= requests.get("http://" + hcl_host + "/api/rooms/" + SmokeSensRoomID, auth=(hcl_user, hcl_password))
                    RoomSResp = json.loads(RoomS.text)
                    RoomName= RoomSResp['name']
                    deviceid = p[i]['id']
                    devicename = p[i]['name']
                    SmokeSensDevEnabled= p[i]['enabled']
                    SmokeDetection= p[i]['properties']['value']
                    SmokeDetectBatteryLevel= float(p[i]['properties']['batteryLevel'])
                    json_body = [
                        {
                            "measurement": "homepi",
                            "tags": {
                                "Device": deviceid,
                                "Name": devicename,
                                "Room" : RoomName
                        
                            },
                            "time": timestamp,
                            "fields": {
                                "DeviceStatus" : SmokeSensDevEnabled,
                                "SmokeDetection": str_to_bool(SmokeDetection),
                                "BatteryLevel": SmokeDetectBatteryLevel
                            }
                        }
                    ]
                    client.write_points(json_body)
                except Exception as e:
                    logging.exception("message")
                    logging.error(e)
            elif 'com.fibaro.binarySwitch' in p[i]['type']:
                #Power Switch Sensors
                try:
                    json_body = None
                    RoomName = None
                    PowerSwitchRoomID = str(p[i]['roomID'])
                    RoomP= requests.get("http://" + hcl_host + "/api/rooms/" + PowerSwitchRoomID, auth=(hcl_user, hcl_password))
                    RoomPResp = json.loads(RoomP.text)
                    RoomName= RoomPResp['name']
                    deviceid = p[i]['id']
                    deviceidS = str(p[i]['id'])
                    devicename = p[i]['name']
                    spower= float(p[i]['properties']['power'])
                    PowerSDevEnabled= p[i]['enabled']
                    senergy= float(p[i]['properties']['energy'])
                    powerEnabled= p[i]['properties']['value']
                
                        #Get Consumption Energy
                    sconsumptionreq= requests.get("http://" + hcl_host + "/api/energy/now/now/summary-graph/devices/power/" + deviceidS, auth=(hcl_user, hcl_password))
                    sconsumptionres= json.loads(sconsumptionreq.text)
                    sconsumption = float(sconsumptionres[0][1])
            
                    #Get Consumption Money
                    sconsumptionreqmoney = requests.get("http://" + hcl_host + "/api/energy/now/now/summary-graph/devices/money/" + deviceidS, auth=(hcl_user, hcl_password))
                    sconsumptionresmoney= json.loads(sconsumptionreqmoney.text)
                    sconsumptionmoney = float(sconsumptionresmoney[0][1])
                    finalmoneyconsumed =  sconsumptionmoney / 1000 * 0.12
                
                    json_body = [
                        {
                            "measurement": "homepi",
                            "tags": {
                                "Device": deviceid,
                                "Name": devicename,
                                "Room" : RoomName
                        
                            },
                            "time": timestamp,
                                "fields": {
                                    "DeviceStatus" : PowerSDevEnabled,
                                    "PowerConsumed": spower,
                                    "EnergyConsumed" : senergy,
                                    "ActualEnergyConsumed" : sconsumption,
                                    "ActualMoneyConsumed" :finalmoneyconsumed,
                                    "PowerPlugIsOn": str_to_bool(powerEnabled)
                                }
                        
                        }
                    ]
                    client.write_points(json_body)
                except Exception as e:
                    logging.exception("message")
                    logging.error(e)

            elif 'com.fibaro.sensor' in p[i]['baseType']:
                #Voltage Sensors
                try:
                    json_body = None
                    RoomName = None
                    VoltageSensRoomID = str(p[i]['roomID'])
                    RoomV= requests.get("http://" + hcl_host + "/api/rooms/" + VoltageSensRoomID , auth=(hcl_user, hcl_password))
                    RoomVResp = json.loads(RoomV.text)
                    RoomName= RoomVResp['name']
                    deviceid = p[i]['id']
                    devicename = p[i]['name']
                    VDevEnabled= p[i]['enabled']
                    VValue= float(p[i]['properties']['value'])
                
                    json_body = [
                        {
                            "measurement": "homepi",
                            "tags": {
                                "Device": deviceid,
                                "Name": devicename,
                                "Room" : RoomName
                        
                            },
                            "time": timestamp,
                            "fields": {
                                "DeviceStatus" : VDevEnabled,
                                "VoltageValue": VValue
                            }
                        }
                    ]
                    client.write_points(json_body)
                except Exception as e:
                    logging.exception("message")
                    logging.error(e)

            
            elif 'com.fibaro.doorWindowSensor' in p[i]['baseType']:
                #Voltage Sensors
                try:
                    json_body = None
                    RoomName = None
                    batterylevel=None
                    armed = None
                    value = None
                    DoorSensRoomID = str(p[i]['roomID'])
                    RoomD= requests.get("http://" + hcl_host + "/api/rooms/" + DoorSensRoomID, auth=(hcl_user, hcl_password))
                    RoomDResp = json.loads(RoomD.text)
                    RoomName= RoomDResp['name']
                    deviceid = p[i]['id']
                    devicename = p[i]['name']
                    DoorSensorEnabled= p[i]['enabled']
                    SensorValue= p[i]['properties']['value']
                    batterylevel = float(p[i]['properties']['batteryLevel'])
                    armed = p[i]['properties']['armed']
                    json_body = [
                    {
                        "measurement": "homepi",
                        "tags": {
                            "Device": deviceid,
                            "Name": devicename,
                            "Room" : RoomName
                        
                        },
                        "time": timestamp,
                        "fields": {
                            "DeviceStatus" : DoorSensorEnabled,
                            "IsDoorOpened": str_to_bool(SensorValue),
                            "BatteryLevel": batterylevel,
                            "IsSensorArmed" : str_to_bool(armed)

                        }
                    }
                ]
                    client.write_points(json_body)
                except Exception as e:
                    logging.exception("message")
                    logging.error(e)
            elif 'com.fibaro.temperatureSensor' in p[i]['type']:
                #Temperature Sensors
                try:
                    json_body = None
                    RoomName = None
                    TempSensRoomID = str(p[i]['roomID'])
                    RoomT= requests.get("http://" + hcl_host + "/api/rooms/" + TempSensRoomID, auth=(hcl_user, hcl_password))
                    RoomTResp = json.loads(RoomT.text)
                    RoomName= RoomTResp['name']
                    deviceid = p[i]['id']
                    devicename = p[i]['name']
                    TempSensDevEnabled= p[i]['enabled']
                    Temp= float(p[i]['properties']['value'])
                
                    json_body = [
                        {
                            "measurement": "homepi",
                            "tags": {
                                "Device": deviceid,
                                "Name": devicename,
                                "Room" : RoomName
                        
                            },
                            "time": timestamp,
                            "fields": {
                                "DeviceStatus" : TempSensDevEnabled,
                                "Temperature": Temp
                            }
                        }
                    ]
                    client.write_points(json_body)
                except Exception as e:
                    logging.exception("message")
                    logging.error(e)
            elif 'com.fibaro.hvac' in p[i]['baseType']:
                #Temperature Sensors
                try:
                    json_body = None
                    RoomName = None
                    AirCSensRoomID = str(p[i]['roomID'])
                    RoomACR= requests.get("http://" + hcl_host + "/api/rooms/" + AirCSensRoomID, auth=(hcl_user, hcl_password))
                    RoomACResp = json.loads(RoomACR.text)
                    RoomName= RoomACResp['name']
                    deviceid = p[i]['id']
                    devicename = p[i]['name']
                    ACDevEnabled= p[i]['enabled']
                    value= float(p[i]['properties']['value'])
                    batterylevel= float(p[i]['properties']['batteryLevel'])
                
                    json_body = [
                        {
                            "measurement": "homepi",
                            "tags": {
                                "Device": deviceid,
                                "Name": devicename,
                                "Room" : RoomName
                        
                            },
                            "time": timestamp,
                            "fields": {
                                "DeviceStatus" : ACDevEnabled,
                                "Temperature": value,
                                "BatteryLevel": batterylevel
                            }
                        }
                    ]
                    client.write_points(json_body)
                except Exception as e:
                    logging.exception("message")
                    logging.error(e)
    time.sleep(90)            