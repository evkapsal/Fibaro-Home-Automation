-- Azure Stream Analytics Query to Azure ML Function for Real time 
-- anomaly detection in Fibaro ZWave Power Plug Sensors.

with aiquery AS (
SELECT
    message.room AS ROOM,
    message.name AS DeviceName,
    CAST(message.PowerConsumed as Float) AS PowerConsumed,
    CAST(message.EnergyConsumed as Float) AS EnergyConsumed,
    CAST(message.ActualEnergyConsumed as Float) AS ActualEnergyConsumed,
    CAST(message.ActualMoneyConsumed as Float) AS ActualMoneyConsumed,
    CAST(message.VoltageValue AS float) AS voltage,
    CAST(message.AmpComsumed AS float) AS AMPS,
    CAST(message.Label AS bigint) AS Label,
    datetime as timestamp,
    DATEADD(hour, 3, CAST(message.time AS datetime)) AS TIME,
    message.DeviceType AS TYPE,
 --Function In Stream Analytics for Anaomaly Detection
    homeAI(
        CAST(message.ActualEnergyConsumed as Float),
        CAST(message.ActualMoneyConsumed as Float),
        CAST(message.AmpComsumed AS float),
        message.name,
        CAST(message.EnergyConsumed as Float),
        CAST(message.Label AS bigint) ,
        CAST(message.PowerConsumed as Float),
        message.room,
        DATEADD(hour, 3, CAST(message.time AS datetime)),
        message.DeviceType,
        CAST(message.VoltageValue AS float)
         )
     as result
    FROM
        myhomeiothub 
    WHERE message.DeviceType = 'binarySensor' AND message.Label = 1
)

Select
    ROOM,
    DeviceName,
    PowerConsumed,
    EnergyConsumed,
    ActualEnergyConsumed,
    ActualMoneyConsumed,
    voltage,
    AMPS,
    Label,
    timestamp,
    TIME,
    TYPE,
    CAST([result].[Scored Labels] as bigint) AS SCORE,
    CAST([result].[Scored Probabilities] as float) AS PROBABILITY
INTO
    AIScorePowerTable  --Return Data to Azure Table Storage
FROM
    aiquery



Select 
    ROOM,
    DeviceName,
    PowerConsumed,
    EnergyConsumed,
    ActualEnergyConsumed,
    ActualMoneyConsumed,
    voltage,
    AMPS,
    Label,
    TIME,
    TYPE,
    CAST([result].[Scored Labels] as bigint) AS SCORE,
    CAST([result].[Scored Probabilities] as float) AS PROBABILITY
INTO
    homeiotbus --Return Data to Azure Service Bus Queue to consume the messages in Logic App.
FROM
    aiquery
    
WHERE CAST([result].[Scored Labels] as bigint) = 1 --Return Only messages that are actual scored as Abnormal.

