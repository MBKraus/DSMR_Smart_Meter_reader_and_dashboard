
import sys
import serial
import pickle
import datetime
import json
import os

# retrieve raw DSMR data via USB port

def retrieve_raw_data():

    print ("Reading DSMR via UBS Port")

    #Set port config
    ser = serial.Serial()
    ser.baudrate = 115200
    ser.bytesize=serial.SEVENBITS
    ser.parity=serial.PARITY_EVEN
    ser.stopbits=serial.STOPBITS_ONE
    ser.xonxoff=0
    ser.rtscts=0
    ser.timeout=20
    ser.port="/dev/ttyUSB0"

    #Open port
    try:
        ser.open()
    except:
        sys.exit ("Can't open port: %s"  % ser.name)

    #Initialize

    data = []

    p1_teller=0

    while p1_teller < 36:
        p1_line=''
    #Read 1 line van de seriele poort
        try:
            p1_raw = ser.readline()
        except:
            sys.exit ("Can't read port: %s" % ser.name )
        p1_str=str(p1_raw)
        p1_line=p1_str.strip()
        data.append(p1_line)
        p1_teller = p1_teller +1

    print ("Signal received")

    #Close port and show status
    try:
        ser.close()
    except:
        sys.exit ("Can't close port" % ser.name )

    return data

def parse_data(raw_data):
    e_laag_kwh = 0
    e_hoog_kwh = 0
    e_huidig_watt = 0
    e_huidig_kwh = 0
    gas_m3 = 0

    for x in raw_data:
        if '1-0:1.8.1' in x:
            try:
                e_laag_kwh = float(x[10:20])
            except:
                with open("exception.p", "wb") as f:
                    pickle.dump(raw_data, f)
        elif '1-0:1.8.2' in x:
            try:
                e_hoog_kwh = float(x[10:20])
            except:
                with open("exception.p", "wb") as f:
                    pickle.dump(raw_data, f)
        elif '1-0:1.7.0' in x:
            try:
                e_huidig_watt = int(x[10:16].replace('.', ''))
                e_huidig_kwh = int(x[10:16].replace('.', '')) / 1000
            except:
                with open("exception.p", "wb") as f:
                    pickle.dump(raw_data, f)
        elif '0-1:24.2.1' in x:
            try:
                gas_m3 = float(x[26:35])
            except:
                with open("exception.p", "wb") as f:
                    pickle.dump(raw_data, f)
        else:
            pass

    return e_laag_kwh, e_hoog_kwh, e_huidig_watt, e_huidig_kwh, gas_m3

def print_data(e_laag_kwh, e_hoog_kwh, e_huidig_watt, e_huidig_kwh, gas_m3):

    print ("Status")
    print("Timestamp: "+str(datetime.datetime.now()))
    print ("#############")
    print('Elektra - Meterstand laag kwh: '+str(e_laag_kwh))
    print('Elektra - Meterstand hoog kwh: '+str(e_hoog_kwh))
    print('Elektra - Huidig verbruik watt: '+str(e_huidig_watt))
    print('Elektra - Huidig verbruik kwh: ' + str(e_huidig_kwh))
    print('Gas meterstand m3: '+str(gas_m3))

def store_data(e_laag_kwh, e_hoog_kwh, e_huidig_watt, gas_m3):

    obs_start=[]
    obs_dict={}

    date_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    date = datetime.datetime.now().date().strftime("%d-%m-%Y")
    time = datetime.datetime.now().time().strftime("%H:%M:%S")
    hour = str(datetime.datetime.now().date)

    obs_dict['date_time'] = date_time
    obs_dict['date'] = date
    obs_dict['time'] = time
    obs_dict['hour'] = hour
    obs_dict['meter_el'] = e_laag_kwh
    obs_dict['meter_eh'] = e_hoog_kwh
    obs_dict['huidig_e'] = e_huidig_watt
    obs_dict['gas'] = gas_m3

    obs_start.append(obs_dict)

    if os.path.isfile('./stored.json'):
        with open('stored.json') as data_file:
            obs = json.load(data_file)

        obs.append(obs_dict)

        with open('stored.json', 'w') as outfile:
            json.dump(obs, outfile)

    else:
        with open('stored.json', 'w') as outfile:
            json.dump(obs_start, outfile)

    print('JSON data stored')


raw_data = retrieve_raw_data()
e_laag_kwh, e_hoog_kwh, e_huidig_watt, e_huidig_kwh, gas_m3 = parse_data(raw_data)
print_data(e_laag_kwh, e_hoog_kwh, e_huidig_watt, e_huidig_kwh, gas_m3)
store_data(e_laag_kwh, e_hoog_kwh, e_huidig_watt, gas_m3)





