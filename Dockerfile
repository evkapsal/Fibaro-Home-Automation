FROM python:3
ADD FibaroIOTService.py /
RUN pip install influxdb
RUN pip install mysql-connector-python
CMD [ "python", "./FibaroIOTService.py" ]
