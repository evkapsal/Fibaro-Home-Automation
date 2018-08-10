SELECT
    message.deviceid AS DeviceID,
    message.room AS ROOM,
    message.name AS DeviceName,
    CAST(message.PowerConsumed as Float) AS PowerConsumed,
    CAST(message.EnergyConsumed as Float) AS EnergyConsumed,
    CAST(message.ActualEnergyConsumed as Float) AS ActualEnergyConsumed,
    CAST(message.ActualMoneyConsumed as Float) AS ActualMoneyConsumed,
    CAST(message.DimLevel as Float) AS DimmerLevel,
    CAST(message.VoltageValue AS Float) AS voltage,
    message.powerplugison AS PowerSwitch,
    message.status AS DeviceStatus,
    CAST(message.Label AS bigint) AS Label,
    DATEADD(hour, 3, CAST(message.time AS datetime)) AS TIME,
    message.DeviceType AS TYPE
INTO
    HomePowertblOUT --YOUR OUTPUT
FROM
    fibaroevents  --YOUR INPUT
WHERE message.DeviceType = 'binarySensor' OR message.DeviceType = 'multilevelSwitch' OR message.DeviceType = 'VoltageSensor'




SELECT
    message.deviceid AS DeviceID,
    message.room AS ROOM,
    message.name AS DeviceName,
    CAST(message.SmokeDetection AS bigint) AS SmokeDetection,
    CAST(message.BatteryLevel as Float) AS BatteryLevel,
    CAST(message.MotionDetected as bigint) AS MotionDetected,
    CAST(message.IsSensorArmed AS bigint) AS SensorArmed,
    CAST(message.IsDoorOpened AS bigint) AS DoorOpened,
    message.status AS DeviceStatus,
    CAST(message.Label AS bigint) AS Label,
    DATEADD(hour, 3, CAST(message.time AS datetime)) AS TIME,
    message.DeviceType AS TYPE
INTO
    HomeSmokeSensortblOUT -YOUR OUTPUT
FROM
    fibaroevents  --YOUR INPUT
WHERE message.DeviceType = 'SmokeSensor' OR message.DeviceType = 'motionsensor' OR message.DeviceType = 'doorSensor'




SELECT
    message.deviceid AS DeviceID,
    message.room AS ROOM,
    message.name AS DeviceName,
    CAST(message.Temperature AS Float) AS Temperature,
    CAST(message.Pressure AS Float) AS Pressure,
    CAST(message.Wind AS Float) AS Wind,
    CAST(message.Humidity AS Float) AS Humidity,
    CAST(message.BatteryLevel as Float) AS BatteryLevel,
    CAST(message.luminance AS Float) AS luminance,
    message.status AS DeviceStatus,
    CAST(message.Label AS bigint) AS Label,
    DATEADD(hour, 3, CAST(message.time AS datetime)) AS TIME,
    message.DeviceType AS TYPE
INTO
    HomeAirConditionOUT -YOUR OUTPUT
FROM
    fibaroevents  --YOUR INPUT
WHERE message.DeviceType = 'airconditionSensor' OR message.DeviceType = 'tempSensor'  OR message.DeviceType = 'OutsideWeather' OR message.DeviceType = 'lightSensor'

SELECT
    message.deviceid AS DeviceID,
    message.room AS ROOM,
    message.name AS DeviceName,
    CAST(message.Bandwidth as bigint) AS Bandwidth,
    message.status AS DeviceStatus,
    CAST(message.Label AS bigint) AS Label,
    DATEADD(hour, 3, CAST(message.time AS datetime)) AS TIME,
    message.DeviceType AS TYPE
INTO
    HomeSwitchSensortbl -YOUR OUTPUT
FROM
    fibaroevents  --YOUR INPUT
WHERE message.DeviceType = 'networkDevice'


SELECT
    message.deviceid AS DeviceID,
    message.room AS ROOM,
    message.name AS DeviceName,
    CAST(message.PowerConsumed as Float) AS PowerConsumed,
    CAST(message.EnergyConsumed as Float) AS EnergyConsumed,
    CAST(message.ActualEnergyConsumed as Float) AS ActualEnergyConsumed,
    CAST(message.ActualMoneyConsumed as Float) AS ActualMoneyConsumed,
    CAST(message.DimLevel as Float) AS DimmerLevel,
    CAST(message.VoltageValue AS Float) AS voltage,
    CAST(message.SmokeDetection AS bigint) AS SmokeDetection,
    CAST(message.BatteryLevel as Float) AS BatteryLevel,
    CAST(message.MotionDetected as bigint) AS MotionDetected,
    CAST(message.IsSensorArmed AS bigint) AS SensorArmed,
    CAST(message.IsDoorOpened AS bigint) AS DoorOpened,
    CAST(message.Temperature AS Float) AS Temperature,
    CAST(message.Bandwidth as bigint) AS Bandwidth,
    CAST(message.Pressure AS Float) AS Pressure,
    CAST(message.Wind AS Float) AS Wind,
    CAST(message.Humidity AS Float) AS Humidity,
    CAST(message.luminance AS Float) AS luminance,
    message.powerplugison AS PowerSwitch,
    message.status AS DeviceStatus,
    CAST(message.Label AS bigint) AS Label,
    DATEADD(hour, 3, CAST(message.time AS datetime)) AS TIME,
    message.DeviceType AS TYPE
INTO 
    myhomeiot -YOUR OUTPUT
FROM
    fibaroevents  --YOUR INPUT

    