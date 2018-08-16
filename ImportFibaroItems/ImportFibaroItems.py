import requests
import json
import calendar
import time
from influxdb import InfluxDBClient
import logging
import datetime
import mysql.connector

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
 
    
#Every minute Get Bandwidth from Devices
def mySQLq (deviceid):
    
    id = str(deviceid)
    dt = datetime.datetime.utcnow()
    time2 = calendar.timegm(dt.utctimetuple())
    time1 = time2 - 60
    tm1= str(time1)
    tm2= str(time2)
    cnx = mysql.connector.connect(user="YOUR-MYSQL-ZABBIX-USERNAME", password="YOUR-MYSQL-ZABBIX-PASSWORD", host="YOUR-ZABBIX-MYSQL-IP", database='zabbix' )
    cnx.autocommit = True
    cursor = cnx.cursor()
    qck= ("SELECT value FROM zabbix.history_uint " 
          "WHERE itemid = %s AND clock BETWEEN %s AND %s GROUP BY clock DIV 1 * 1 ORDER BY clock desc")
    f= cursor.execute(qck, (id, tm1, tm2))
    r= str(cursor.fetchone())
    re= r.replace(",","")
    result = json.dumps({"DeviceID": id, "Bandwidth": re, "Timestamp": str(dt)})
    result = result.replace("(","")
    result = result.replace(")","")
    cursor.close()
    cnx.close()
    return result

#Country KW price
kwmoneyvalue = 0.12

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

class powerSensor(object):
    def __init__(self, name, room, time, EnergyConsumed, AmpComsumed, VoltageValue, ActualEnergyConsumed , ActualMoneyConsumed, Label , PowerConsumed):
        self.time = time
        self.name = name
        self.room = room
        self.EnergyConsumed = EnergyConsumed
        self.AmpComsumed = AmpComsumed
        self.VoltageValue = VoltageValue
        self.ActualEnergyConsumed  = ActualEnergyConsumed 
        self.ActualMoneyConsumed = ActualMoneyConsumed
        self.Label = Label
        self.PowerConsumed = PowerConsumed
        self.DeviceType = "binarySensor"
    
    def addmilisecadd(self):
        fdate= str(datetime.datetime.utcnow() + datetime.timedelta(microseconds=35))
        return fdate
    def addmilisecmin(self):
        ndate= str(datetime.datetime.utcnow() - datetime.timedelta(microseconds=35))
        return ndate
    #Function to send fake data for Azure ML Training
    def sendFakeDataForMLTrainingA(self):
        self.time = time
        self.name = name
        self.room = room
        self.EnergyConsumed = EnergyConsumed + 235
        self.AmpComsumed = AmpComsumed + 6
        self.VoltageValue = VoltageValue + 89
        self.ActualEnergyConsumed  = ActualEnergyConsumed + 365 
        self.ActualMoneyConsumed = ActualMoneyConsumed + 7.8
        self.Label = 0
        self.PowerConsumed = PowerConsumed
        self.DeviceType = "binarySensor"
        return self
    def sendFakeDataForMLTrainingB(self):
        self.time = time
        self.name = name
        self.room = room
        self.EnergyConsumed = EnergyConsumed - 235
        self.AmpComsumed = AmpComsumed - 6
        self.VoltageValue = VoltageValue - 89
        self.ActualEnergyConsumed  = ActualEnergyConsumed - 365 
        self.ActualMoneyConsumed = ActualMoneyConsumed - 7.8
        self.Label = 0
        self.PowerConsumed = PowerConsumed
        self.DeviceType = "binarySensor"
        return self


class ioSensor(object):
    def __init__(self, name, room, time, motionId, motionValue, motionBatValue, doorId, doorValue , doorBatteryValue, smokeId, smokeValue, smokeBatteryValue, Label):
        self.time = time
        self.name = name
        self.room = room
        self.motionId = motionId
        self.motionValue = motionValue
        self.motionBatValue = motionBatValue
        self.doorId = doorId
        self.doorValue  = doorValue 
        self.doorBatteryValue = doorBatteryValue
        self.smokeId = smokeId
        self.smokeValue = smokeValue
        self.smokeBatteryValue = smokeBatteryValue
        self.Label = Label
        self.DeviceType = "ioSensor"

    def addmilisecadd(self):
        fdate= str(datetime.datetime.utcnow() + datetime.timedelta(microseconds=35))
        return fdate
    def addmilisecmin(self):
        ndate= str(datetime.datetime.utcnow() - datetime.timedelta(microseconds=35))
        return ndate

class tempSensor(object):
    def __init__(self, name, room, time, tempId, tempValue, humId, humValue , luxId, luxValue, lightId, lightEnergy, lightPower, lightDimValue, Label):
        self.time = time
        self.name = name
        self.room = room
        self.tempId = tempId
        self.tempValue = tempValue
        self.humId = humId
        self.humValue = humValue
        self.luxId = luxId
        self.luxValue = luxValue
        self.lightId = lightId
        self.lightDimValue = lightDimValue
        self.lightEnergy = lightEnergy
        self.lightPower = lightPower
        self.Label = Label
        self.DeviceType = "tempSensor"

    def addmilisecadd(self):
        fdate= str(datetime.datetime.utcnow() + datetime.timedelta(microseconds=35))
        return fdate
    def addmilisecmin(self):
        ndate= str(datetime.datetime.utcnow() - datetime.timedelta(microseconds=35))
        return ndate

class netSensor(object):
    def __init__(self, name, room, time, netId, netValue, Label ):
        self.time = time
        self.name = name
        self.room = room
        self.netId = netId
        self.netValue = netValue
        self.Label = Label
        self.DeviceType = "netSensor"

    def addmilisecadd(self):
        fdate= str(datetime.datetime.utcnow() + datetime.timedelta(microseconds=35))
        return fdate
    def addmilisecmin(self):
        ndate= str(datetime.datetime.utcnow() - datetime.timedelta(microseconds=35))
        return ndate

while True:
    #Start Devices Processing --> Grafana
    json_propertyvalues = requests.get("http://" + hcl_host + "/api/devices", auth=(hcl_user, hcl_password))
    p = json.loads(json_propertyvalues.text)
    l = len(p)

    client = InfluxDBClient(host, port, user, password, dbname,retries=3)
    timestamp = calendar.timegm(time.gmtime()) * 1000000000
    dateTime = str(datetime.datetime.utcnow())

    #Start Room Processing   --> Azure Iot Hub
    homeRoomsRequest = requests.get("http://" + hcl_host + "/api/rooms", auth=(hcl_user, hcl_password))
    homeRooms= json.loads(homeRoomsRequest.text)
    h= len(homeRooms)

    #Start Azure Iot Hub Process
    for s in range(0,h):
        #Get Devices per Room
        homeRoomId = str(homeRooms[s]['id'])
        homeRoomName= str(homeRooms[s]['name'])
                
        #Collect Motion Sensors
        motionSensors = []

        try:
            motionSensorsFibaroRequest = requests.get("http://" + hcl_host + "/api/devices/?roomID=" + homeRoomId +"&type=com.fibaro.FGMS001v2",  auth=(hcl_user, hcl_password))
            dateTime = str(datetime.datetime.utcnow())
        except Exception as c:
            logging.error(c)
        finally:
            strf=len(motionSensorsFibaroRequest.text)
            if strf > 2 :
                fmotionSensorsobjs= json.loads(motionSensorsFibaroRequest.text)
                f= len(fmotionSensorsobjs)
                if f > 0:
                    for o in range(0,f):
                        motionSensors.append(fmotionSensorsobjs[o])
                else:
                    motionSensors.append(fmotionSensorsobjs[0])                      
        try:
            otherMotionSensorsRequest = requests.get("http://" + hcl_host + "/api/devices/?roomID=" + homeRoomId +"&type=com.fibaro.motionSensor",  auth=(hcl_user, hcl_password))
        except Exception as c:
            logging.error(c) 
        finally:
            stre=len(otherMotionSensorsRequest.text)
            if stre > 2 :
                omotionSensorsobjs= json.loads(otherMotionSensorsRequest.text)
                k= len(omotionSensorsobjs)
                if k > 0:
                    for q in range(0,k):
                        motionSensors.append(omotionSensorsobjs[q])
                else:
                    motionSensors.append(omotionSensorsobjs[0])    
          

        try:
            oftherMotionSensorsRequest = requests.get("http://" + hcl_host + "/api/devices/?roomID=" + homeRoomId +"&baseType=com.fibaro.motionSensor",  auth=(hcl_user, hcl_password))
        except Exception as c:
            logging.error(c)
        finally:
            strg=len(oftherMotionSensorsRequest.text)
            if strg > 2 :
                ofmotionSensorsobjs= json.loads(oftherMotionSensorsRequest.text)
                u= len(ofmotionSensorsobjs)
                if u > 0:
                    for y in range(0,u):
                        motionSensors.append(ofmotionSensorsobjs[y])
                else:
                    motionSensors.append(ofmotionSensorsobjs[0])
        

        #Collect Door Sensors
        doorSensors = []

        try:
            doorSensorsFibaroRequest = requests.get("http://" + hcl_host + "/api/devices/?roomID=" + homeRoomId +"&baseType=com.fibaro.doorWindowSensor",  auth=(hcl_user, hcl_password))
        except Exception as c:
            logging.error(c) 
        finally:
            strh=len(doorSensorsFibaroRequest.text)
            if strh > 2 :
                doorSensorsobjs= json.loads(doorSensorsFibaroRequest.text)
                x= len(doorSensorsobjs)
                if x > 0:
                    for z in range(0,x):
                        doorSensors.append(doorSensorsobjs[z])
                else:
                    doorSensors.append(doorSensorsobjs[0])
        #Collect Smoke Sensors
        smokeSensors = []

        try:
            smokeSensorsFibaroRequest = requests.get("http://" + hcl_host + "/api/devices/?roomID=" + homeRoomId +"&type=com.fibaro.smokeSensor",  auth=(hcl_user, hcl_password))
        except Exception as c:
            logging.error(c) 
        finally:
            strj=len(smokeSensorsFibaroRequest.text)
            if strj > 2 :
                smokeSensorsobjs= json.loads(smokeSensorsFibaroRequest.text)
                d= len(smokeSensorsobjs)
                if d > 0:
                    for r in range(0,d):
                        smokeSensors.append(smokeSensorsobjs[r])
                else:
                    smokeSensors.append(smokeSensorsobjs[0])
        #Process Sensor Objects

        m1= len(motionSensors)
        d1= len(doorSensors)
        s1= len(smokeSensors)
        sFinal= [m1,d1,s1]
        maxS= max(sFinal)

        if maxS > 0:
           for j in range(0, maxS):
            try:
                if m1 > 0:
                    try:
                        motionSensorID= motionSensors[j]['id']
                        motionValue= str_to_bool(motionSensors[j]['properties']['value'])
                        motionBatteryValue = motionSensors[j]['properties']['batteryLevel']
                        motionSensorname = motionSensors[j]['name']
                    except IndexError:
                        motionSensorID= 0
                        motionValue= 0
                        motionBatteryValue= 0
                else:
                    motionSensorID= 0
                    motionValue= 0
                    motionBatteryValue= 0
               
                if d1 > 0:
                    try:
                       doorSensorID=doorSensors[j]["id"]
                       doorSensorValue = str_to_bool(doorSensors[j]['properties']['value'])
                       doorBatteryValue = motionSensors[j]['properties']['batteryLevel']
                       motionSensorname = doorSensors[j]['name']
                    except IndexError:
                        doorSensorID= 0
                        doorSensorValue= 0
                        doorBatteryValue = 0
                else:
                    doorSensorID= 0
                    doorSensorValue= 0
                    doorBatteryValue = 0

                if s1 > 0:
                    try:
                       smokeSensorID=smokeSensors[j]["id"]
                       smokeSensorValue = str_to_bool(smokeSensors[j]['properties']['value'])
                       smokeBatteryValue = motionSensors[j]['properties']['batteryLevel']
                       motionSensorname = smokeSensors[j]['name']
                    except IndexError:
                        smokeSensorID= 0
                        smokeSensorValue= 0
                        smokeBatteryValue = 0
                else:
                    smokeSensorID= 0
                    smokeSensorValue= 0
                    smokeBatteryValue = 0
                
                ioSensorObj= ioSensor(name=motionSensorname, time=dateTime, room= homeRoomName, motionId= motionSensorID, motionValue= motionValue, motionBatValue=motionBatteryValue, doorId= doorSensorID, doorValue= doorSensorValue, doorBatteryValue= doorBatteryValue, smokeId= smokeSensorID, smokeValue= smokeSensorValue, smokeBatteryValue=smokeBatteryValue, Label= 1) 
                smessage = json.dumps(ioSensorObj.__dict__)
                sendIOTmessage(json.loads(smessage))
                #print(smessage)
            except Exception as c:
                logging.error(c)
        
        #Collect Temp Sensors
        tempSensors = []

        try:
            tempSensorsFibaroRequest = requests.get("http://" + hcl_host + "/api/devices/?roomID=" + homeRoomId +"&type=com.fibaro.temperatureSensor",  auth=(hcl_user, hcl_password))
        except Exception as c:
            logging.error(c)
        finally:
            strk=len(tempSensorsFibaroRequest.text)
            if strk > 2 :
                tempSensorsobjs= json.loads(tempSensorsFibaroRequest.text)
                f= len(tempSensorsobjs)
                if f > 0:
                    for o in range(0,f):
                        tempSensors.append(tempSensorsobjs[o])
                else:
                    tempSensors.append(tempSensorsobjs[0]) 

        try:
            otempSensorsFibaroRequest = requests.get("http://" + hcl_host + "/api/devices/?roomID=" + homeRoomId +"&type=com.fibaro.yrWeather",  auth=(hcl_user, hcl_password))
        except Exception as c:
            logging.error(c)
        finally:
            str2=len(otempSensorsFibaroRequest.text)
            if str2 > 2 :
                otempSensorsobjs= json.loads(otempSensorsFibaroRequest.text)
                f= len(otempSensorsobjs)
                if f > 0:
                    for o in range(0,f):
                        tempSensors.append(otempSensorsobjs[o])
                else:
                    tempSensors.append(otempSensorsobjs[0])

        try:
            htempSensorsFibaroRequest = requests.get("http://" + hcl_host + "/api/devices/?roomID=" + homeRoomId +"&type=com.fibaro.humiditySensor",  auth=(hcl_user, hcl_password))
        except Exception as c:
            logging.error(c)
        finally:
            stra=len(htempSensorsFibaroRequest.text)
            if stra > 2 :
                htempSensorsobjs= json.loads(htempSensorsFibaroRequest.text)
                f= len(htempSensorsobjs)
                if f > 0:
                    for o in range(0,f):
                        tempSensors.append(htempSensorsobjs[o])
                else:
                    tempSensors.append(htempSensorsobjs[0])
        
        #Collect Lux Sensors
        luxSensors = []

        try:
            luxSensorsFibaroRequest = requests.get("http://" + hcl_host + "/api/devices/?roomID=" + homeRoomId +"&type=com.fibaro.lightSensor",  auth=(hcl_user, hcl_password))
        except Exception as c:
            logging.error(c)
        finally:
            strb=len(luxSensorsFibaroRequest.text)
            if strb > 2 :
                luxSensorsobjs= json.loads(luxSensorsFibaroRequest.text)
                f= len(luxSensorsobjs)
                if f > 0:
                    for o in range(0,f):
                        luxSensors.append(luxSensorsobjs[o])
                else:
                    luxSensors.append(luxSensorsobjs[0])
                    
        #Collect Lights Sensors
        lightsSensors = []

        try:
            lightsSensorsFibaroRequest = requests.get("http://" + hcl_host + "/api/devices/?roomID=" + homeRoomId +"&type=com.fibaro.multilevelSwitch",  auth=(hcl_user, hcl_password))
        except Exception as c:
            logging.error(c)
        finally:
            strc=len(lightsSensorsFibaroRequest.text)
            if strc > 2 :
                lightsSensorsobjs= json.loads(lightsSensorsFibaroRequest.text)
                f= len(lightsSensorsobjs)
                if f > 0:
                    for o in range(0,f):
                        lightsSensors.append(lightsSensorsobjs[o])
                else:
                    lightsSensors.append(lightsSensorsobjs[0])

        try:
            olightsSensorsFibaroRequest = requests.get("http://" + hcl_host + "/api/devices/?roomID=" + homeRoomId +"&baseType=com.fibaro.multilevelSwitch",  auth=(hcl_user, hcl_password))
        except Exception as c:
            logging.error(c)
        finally:
            str1= len(olightsSensorsFibaroRequest.text)
            if str1 > 2:
                olightsSensorsobjs= json.loads(olightsSensorsFibaroRequest.text)
                f= len(olightsSensorsobjs)
                if f > 0:
                    for o in range(0,f):
                        lightsSensors.append(olightsSensorsobjs[o])
                else:
                    lightsSensors.append(olightsSensorsobjs[0])
                    
        
        #Process Sensor Objects

        a1= len(tempSensors)
        b1= len(luxSensors)
        c1= len(lightsSensors)
        cFinal= [a1,b1,c1]
        maxC= max(cFinal)

        if maxC > 0:
           for j in range(0, maxC):
            try:
                if a1 > 0:
                    try:
                        sensorName = tempSensors[j]['name']
                        if  "com.fibaro.yrWeather" in tempSensors[j]['type']:
                            humidityId = tempSensors[j]['id']
                            humidityValue = tempSensors[j]['properties']["Humidity"]
                            
                        elif "com.fibaro.humiditySensor" in tempSensors[j]['type']:
                            humidityId = tempSensors[j]['id']
                            humidityValue = tempSensors[j]['properties']["value"]
                           
                        else:
                            humidityValue = 0
                            humidityId = 0
                            tempSensorID= tempSensors[j]['id']
                            tempValue= tempSensors[j]['properties']['value']
                        
                    except IndexError:
                        tempSensorID= 0
                        tempValue= 0
                        humidityId = 0
                        humidityValue = 0
                else:
                    tempSensorID= 0
                    tempValue= 0
                    humidityId = 0
                    humidityValue = 0
               
                if b1 > 0:
                    try:
                       sensorName = luxSensors[j]['name']
                       luxSensorID=luxSensors[j]["id"]
                       luxSensorValue = luxSensors[j]['properties']['value']
                    except IndexError:
                        luxSensorID= 0
                        luxSensorValue= 0
                else:
                    luxSensorID= 0
                    luxSensorValue= 0

                if c1 > 0:
                    try:
                        sensorName = lightsSensors[j]['name']

                        if "com.fibaro.multilevelSwitch" in lightsSensors[j]['type']:
                            lightsEnergy= 0
                            lightsPower = 0
                            lightsSensorValue= lightsSensors[j]['properties']['value']
                            lightsSensorID=lightsSensors[j]["id"]
                            
                        else:
                           lightsSensorID=lightsSensors[j]["id"]
                           lightsSensorValue = lightsSensors[j]['properties']['value']
                           lightsEnergy = lightsSensors[j]['properties']['energy']
                           lightsPower =  lightsSensors[j]['properties']['power']

                    except IndexError:
                        lightsSensorID= 0
                        lightsSensorValue= 0
                        lightsEnergy = 0
                        lightsPower = 0
                else:
                    lightsSensorID= 0
                    lightsSensorValue= 0
                    lightsEnergy = 0
                    lightsPower = 0
                
                lightsSensorObj= tempSensor(name=sensorName,room=homeRoomName,time= dateTime, tempId= tempSensorID, tempValue= tempValue, humId= humidityId, humValue= humidityValue, luxId= luxSensorID, luxValue= luxSensorValue, lightId= lightsSensorID, lightEnergy= lightsEnergy, lightPower= lightsPower, lightDimValue= lightsSensorValue, Label= 1)
                tmessage = json.dumps(lightsSensorObj.__dict__)
                sendIOTmessage(json.loads(tmessage))
                #print(tmessage)
            except Exception as c:
                logging.error(c)
        
        #Collect Power Sensors
        powerSensors = []
        
        try:
            powerSensorsFibaroRequest = requests.get("http://" + hcl_host + "/api/devices/?roomID=" + homeRoomId +"&type=com.fibaro.binarySwitch",  auth=(hcl_user, hcl_password))
        except Exception as c:
            logging.error(c)
        finally:
            strd=len(powerSensorsFibaroRequest.text)
            if strd > 2 :
                powerSensorsobjs= json.loads(powerSensorsFibaroRequest.text)
                f= len(powerSensorsobjs)
                if f > 0:
                    for o in range(0,f):
                        powerSensors.append(powerSensorsobjs[o])
                else:
                    powerSensors.append(powerSensorsobjs[0])
        #Process Sensor Objects
        n1= len(powerSensors)

        if n1 >0:
            for i in range(0, n1):
                if 'isLight' not in powerSensors[i]['properties'].keys():
                    #Power Switch Sensors
                    try:
                        #Continue Object Process
                        deviceId = powerSensors[i]['id']
                        deviceIdS = str(powerSensors[i]['id'])
                        deviceName = powerSensors[i]['name']
                        sPower= float(powerSensors[i]['properties']['power'])
                        sEnergy= float(powerSensors[i]['properties']['energy'])

                        #Get Consumption Energy from Graph
                        sconsumptionreq= requests.get("http://" + hcl_host + "/api/energy/now/now/summary-graph/devices/power/" + deviceIdS, auth=(hcl_user, hcl_password))
                        sconsumptionres= json.loads(sconsumptionreq.text)
                        sconsumption = float(sconsumptionres[0][1])
            
                        #Get Consumption Money from Graph [kwmoneyvalue] country price per KW/h --> you can find this variable at the beggining of the script.
                        sconsumptionreqmoney = requests.get("http://" + hcl_host + "/api/energy/now/now/summary-graph/devices/money/" + deviceIdS, auth=(hcl_user, hcl_password))
                        sconsumptionresmoney= json.loads(sconsumptionreqmoney.text)
                        sconsumptionmoney = float(sconsumptionresmoney[0][1])
                        finalmoneyconsumed =  sconsumptionmoney / 1000 * kwmoneyvalue

                        #Get Parent Device 
                        parentId= str(powerSensors[i]['parentId'])
                        parentDevice=  requests.get("http://" + hcl_host + "/api/devices/?parentId=" + parentId,  auth=(hcl_user, hcl_password))

                        #Get Reference devices
                        parentObject = json.loads(parentDevice.text)
                        t = len(parentObject)
                        for i in range(0, t):
                            if 'unit' in parentObject[i]['properties'].keys():
                                if 'A' in parentObject[i]['properties']['unit']:
                                    amp= float(parentObject[i]['properties']['value'])
                                elif 'V' in parentObject[i]['properties']['unit']:
                                    volt= float(parentObject[i]['properties']['value'])
                
                        deviceObj = powerSensor(name= deviceName, room= homeRoomName, time=dateTime, AmpComsumed= amp, EnergyConsumed=sEnergy, VoltageValue= volt, ActualEnergyConsumed= sconsumption, ActualMoneyConsumed= finalmoneyconsumed, Label= 1, PowerConsumed=sPower)
                        vmessage = json.dumps(deviceObj.__dict__)
                        sendIOTmessage(json.loads(vmessage))
                        #print(vmessage)

                    except Exception as e:
                        logging.error(e)

    #start network objects
    netObjects= []
        
    #Net Object IDs
    iptvId = "23792"
    homeId = "23775"
    netdevicesId = "23791"

    #Add Objects to List/Array
    netObjects.append(iptvId)
    netObjects.append(homeId)
    netObjects.append(netdevicesId)

    n= len(netObjects)
    if n > 0:
        for k in range(0, n):
        #Process Net Object
            try:
                netobjId = netObjects[k]
                resQ= json.loads(mySQLq(netobjId))
                while  resQ['Bandwidth'] == "None":
                    resQ= json.loads(mySQLq(netobjId))

                if '23792' in resQ['DeviceID']:
                    netDeviceName = "OTE TV"
                    netDeviceRoom = "Main"
                    netBandwidth = str(resQ['Bandwidth'])

                elif '23775' in resQ['DeviceID']:
                    netDeviceName = "Home"
                    netDeviceRoom = "Main"
                    netBandwidth = str(resQ['Bandwidth'])

                elif '23791' in resQ['DeviceID']:
                    netDeviceName = "Network Devices"
                    netDeviceRoom = "Main"
                    netBandwidth = str(resQ['Bandwidth'])

                netObjectS = netSensor(name=netDeviceName, netId=netobjId, room= netDeviceRoom, time= dateTime, netValue=netBandwidth, Label= 1)
                jmessage = json.dumps(netObjectS.__dict__)
                sendIOTmessage(json.loads(jmessage))
                #print(jmessage)
            except Exception as e:
                    logging.error(e)    



    #Start Grafana Process
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
                                    "DeviceStatus" : WeatherDevEnabled,
                                    "DeviceType": "OutsideWeather",
									"Label": 1
                                }
                            }
                        ]
                    client.write_points(json_body)
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
                    finalmoneyconsumed =  consumptionmoney / 1000 * kwmoneyvalue

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
                                    "ActualMoneyConsumed" : consumptionmoney,
                                    "DeviceType": "multilevelSwitch"
                                }
                            }
                        ]
                    client.write_points(json_body)
                except Exception as e:
                    logging.error(e)
            elif 'com.fibaro.motionSensor' in p[i]['baseType'] or 'com.fibaro.motionSensor' in p[i]['type'] or 'com.fibaro.FGMS001v2' in p[i]['type'] :
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
                                "MotionDetected" :str_to_bool(motiondetect)
                                
                            }
                        }
                    ]
                    client.write_points(json_body)
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
            elif 'com.fibaro.binarySwitch' in p[i]['type']:
                #if not hasattr((p[i]['properties']), 'isLight'):
                if 'isLight' not in p[i]['properties'].keys():
                    #Power Switch Sensors
                    try:
                        PowerSwitchRoomID = str(p[i]['roomID'])
                        RoomP= requests.get("http://" + hcl_host + "/api/rooms/" + PowerSwitchRoomID, auth=(hcl_user, hcl_password))

                        #Continue Object
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
                        finalmoneyconsumed =  sconsumptionmoney / 1000 * kwmoneyvalue


                        #Send Data to InfluxDB
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
                            "IsSensorArmed" : str_to_bool(armed),
                            "DeviceType": "doorSensor"
                           
                            

                        }
                    }
                ]
                    client.write_points(json_body)
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
            elif 'com.fibaro.humiditySensor' in p[i]['type']:
                #Humidity Sensors
                try:
                    json_body = None
                    RoomName = None
                    HumSensRoomID = str(p[i]['roomID'])
                    RoomT= requests.get("http://" + hcl_host + "/api/rooms/" + HumSensRoomID, auth=(hcl_user, hcl_password))
                    RoomTResp = json.loads(RoomT.text)
                    RoomName= RoomTResp['name']
                    deviceid = p[i]['id']
                    devicename = p[i]['name']
                    HumSensDevEnabled= p[i]['enabled']
                    RHumidity= float(p[i]['properties']['value'])
                
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
                                "DeviceStatus" : HumSensDevEnabled,
                                "Humidity": RHumidity
                            }
                        }
                    ]
                    client.write_points(json_body)
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


     

    time.sleep(30)
   
