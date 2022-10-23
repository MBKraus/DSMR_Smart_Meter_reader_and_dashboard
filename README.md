# Slimme Meter (DSMR v5) Reader + Dashboard

Requirementsss:

- Dash (inc. Plotly)
- Pandas
- Python 3.6.6
- Raspberry Pi connected to DSMR via USB

Installation / deployment:

- put read.py and dashboard.py on your Raspberry Pi
- create a virtual environment that has the packages above installed and activate it
- schedule a task with Cron that periodically run reads.py, so that data is extracted from the DSMR (via UBS) and stored. One way to do this is to open crontab by means of `crontab -e` and insert the following task `0 * * * * python <path to read.py> >/dev/null 2>&1`. With this task data is retrieved every hour.
- run the dashboard with a nohup command (and access it via the IP of your Rpi & port 8050)


![alt text](https://github.com/MBKraus/Slimme_meter_reader-dashboard/blob/master/dasbhoard.png)
