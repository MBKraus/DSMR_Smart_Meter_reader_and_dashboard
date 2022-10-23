# Slimme Meter (DSMR v5) Reader + Dashboard

Requirements:

- pandas==1.5.0
- dash==2.6.2
- pyserial==3.5
- Raspberry Pi connected to DSMR via USB

Installation / deployment:

- clone the repo on your Raspberry Pi
- create a virtual environment that has the packages in the `requirements.txt` installed
- schedule a Cron task that periodically activates the virtual environment and runs `get_data.py`, so that data is extracted from the DSMR (via UBS) and stored.
- schedule a Cron task that periodically refreshes/restarts the dashboard (see `restart_script.sh` for an example of such a script).


![alt text](https://github.com/MBKraus/Slimme_meter_reader-dashboard/blob/master/dasbhoard.png)
