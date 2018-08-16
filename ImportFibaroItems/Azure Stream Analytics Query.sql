
--Send Data to Power BI 
--To Configure the correct time please change the DATEADD(hour [#number]) cause of UTC Convertion
SELECT
    message.deviceid AS DeviceID,
    message.room AS ROOM,
    message.name AS DeviceName,
    CAST(message.PowerConsumed as Float) AS PowerConsumed,
    CAST(message.EnergyConsumed as Float) AS EnergyConsumed,
    CAST(message.ActualEnergyConsumed as Float) AS ActualEnergyConsumed,
    CAST(message.ActualMoneyConsumed as Float) AS ActualMoneyConsumed,
    CAST(message.VoltageValue AS Float) AS voltage,
    CAST(message.AmpComsumed AS Float) AS AMPS,
    CAST(message.motionId as bigint) AS MotionSensorID,
    CAST(message.motionValue as bigint) AS MotionSensorValue,
    CAST(message.motionBatteryValue as float) AS MotionSensorBatteryLevel,
    CAST(message.doorId as bigint) AS DoorSensorID,
    CAST(message.doorValue as bigint) AS DoorSensorValue,
    CAST(message.motionBatValue as float) AS DoorSensorBatteryLevel,
    CAST(message.smokeId AS bigint) AS SmokeSensorID,
    CAST(message.smokeValue AS bigint) AS SmokeSensorValue,
    CAST(message.smokeBatteryValue as float) AS SmokeSensorBatteryLevel,
    CAST(message.tempId as bigint) AS TempSensorID,
    CAST(message.tempValue as float) AS TempSensorValue,
    CAST(message.humId as bigint) AS HumiditySensorID,
    CAST(message.humValue as float) AS HumiditySensorValue,
    CAST(message.luxId AS bigint) AS LuxSensorID,
    CAST(message.luxValue AS float) AS LuxSensorValue,
    CAST(message.lightId AS bigint) AS LightSensorID,
    CAST(message.lightDimValue AS float) AS LightSensorDimValue,
    CAST(message.lightEnergy AS float) AS LightSensorEnergy,
    CAST(message.lightPower AS float) AS LightSensorPower,
    CAST(message.netId as bigint) AS NetworkDeviceID,
    CAST(message.netValue as float) AS NetworkDeviceBandwidthValue,
    CAST(message.Label AS bigint) AS Label,
    DATEADD(hour, 3, CAST(message.time AS datetime)) AS TIME,
    message.DeviceType AS TYPE
INTO
    myhomeiot
FROM
    fibaroevents Partition By PartitionId

--Select Power Sensors and Send it to Azure Table Storage
--To Configure the correct time please change the DATEADD(hour [#number]) cause of UTC Convertion
SELECT
    message.room AS ROOM,
    message.name AS DeviceName,
    CAST(message.PowerConsumed as Float) AS PowerConsumed,
    CAST(message.EnergyConsumed as Float) AS EnergyConsumed,
    CAST(message.ActualEnergyConsumed as Float) AS ActualEnergyConsumed,
    CAST(message.ActualMoneyConsumed as Float) AS ActualMoneyConsumed,
    CAST(message.VoltageValue AS Float) AS voltage,
    CAST(message.AmpComsumed AS Float) AS AMPS,
    CAST(message.Label AS bigint) AS Label,
    DATEADD(hour, 3, CAST(message.time AS datetime)) AS TIME,
    message.DeviceType AS TYPE,
    datetime as timestamp
INTO
    HomeIOTPower 
FROM
    fibaroevents  
WHERE message.DeviceType = 'binarySensor'

--Select IO Sensorsand Send it to Azure Table Storage
--To Configure the correct time please change the DATEADD(hour [#number]) cause of UTC Convertion
SELECT
    message.room AS ROOM,
    message.name AS DeviceName,
    CAST(message.motionId as bigint) AS MotionSensorID,
    CAST(message.motionValue as bigint) AS MotionSensorValue,
    CAST(message.motionBatValue as float) AS MotionSensorBatteryLevel,
    CAST(message.doorId as bigint) AS DoorSensorID,
    CAST(message.doorValue as bigint) AS DoorSensorValue,
    CAST(message.doorBatteryValue as float) AS DoorSensorBatteryLevel,
    CAST(message.smokeId AS bigint) AS SmokeSensorID,
    CAST(message.smokeValue AS bigint) AS SmokeSensorValue,
    CAST(message.smokeBatteryValue as float) AS SmokeSensorBatteryLevel,
    CAST(message.Label AS bigint) AS Label,
    DATEADD(hour, 3, CAST(message.time AS datetime)) AS TIME,
    message.DeviceType AS TYPE,
    datetime as timestamp
INTO
    HomeIOTio
FROM
    fibaroevents  
WHERE message.DeviceType = 'ioSensor'

--Select Temp Sensorsand Send it to Azure Table Storage
--To Configure the correct time please change the DATEADD(hour [#number]) cause of UTC Convertion
SELECT
    message.room AS ROOM,
    message.name AS DeviceName,
    CAST(message.tempId as bigint) AS TempSensorID,
    CAST(message.tempValue as float) AS TempSensorValue,
    CAST(message.humId as bigint) AS HumiditySensorID,
    CAST(message.humValue as float) AS HumiditySensorValue,
    CAST(message.luxId AS bigint) AS LuxSensorID,
    CAST(message.luxValue AS float) AS LuxSensorValue,
    CAST(message.lightId AS bigint) AS LightSensorID,
    CAST(message.lightDimValue AS float) AS LightSensorDimValue,
    CAST(message.lightEnergy AS float) AS LightSensorEnergy,
    CAST(message.lightPower AS float) AS LightSensorPower,
    CAST(message.Label AS bigint) AS Label,
    DATEADD(hour, 3, CAST(message.time AS datetime)) AS TIME,
    message.DeviceType AS TYPE,
    datetime as timestamp
INTO
    HomeIOTTemp
FROM
    fibaroevents  
WHERE message.DeviceType = 'tempSensor'


--Select Network Sensorsand Send it to Azure Table Storage
--To Configure the correct time please change the DATEADD(hour [#number]) cause of UTC Convertion

SELECT
    message.room AS ROOM,
    message.name AS DeviceName,
    CAST(message.netId as bigint) AS NetworkDeviceID,
    CAST(message.netValue as float) AS NetworkDeviceBandwidthValue,
    CAST(message.Label AS bigint) AS Label,
    DATEADD(hour, 3, CAST(message.time AS datetime)) AS TIME,
    message.DeviceType AS TYPE,
    datetime as timestamp
INTO
    HomeIOTNet
FROM
    fibaroevents  
WHERE message.DeviceType = 'netSensor'

    
