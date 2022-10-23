import pandas as pd
import sys
import serial
import datetime
import json
import os
import logging

logger = logging.getLogger('data_parser')
logger.setLevel(logging.INFO)

class DataFetcher():

	def __init__(self, source_json_path):
		self.source_json_path = source_json_path

	def fetch_raw_data(self):

		logger.info("Reading DSMR via UBS Port")

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
		except Exception as e:
			logger.exception(e)
			sys.exit("Can't open port: %s"  % ser.name)

		#Initialize

		data = []

		p1_teller=0

		while p1_teller < 36:
			#Read 1 line van de seriele poort
			try:
				p1_raw = ser.readline()
				p1_str=str(p1_raw).strip()
				data.append(p1_str)
			except Exception as e:
				logger.exception(e)
				sys.exit ("Can't read port: %s" % ser.name )

			p1_teller = p1_teller +1

		logger.info("Signal received")

		#Close port and show status
		try:
			ser.close()
			self.raw_data = data
		except Exception as e:
			logger.exception(e)
			sys.exit("Can't close port" % ser.name)


	def parse_data(self):
		e_laag_kwh = 0
		e_hoog_kwh = 0
		e_huidig_watt = 0
		e_huidig_kwh = 0
		gas_m3 = 0

		for x in self.raw_data:
			if '1-0:1.8.1' in x:
				try:
					e_laag_kwh = float(x[12:22])
				except Exception as e:
					logger.exception(e)
			elif '1-0:1.8.2' in x:
				try:
					e_hoog_kwh = float(x[12:22])
				except Exception as e:
					logger.exception(e)
			elif '1-0:1.7.0' in x:
				try:
					e_huidig_watt = int(x[12:18].replace('.', ''))
					e_huidig_kwh = int(x[12:18].replace('.', '')) / 1000
				except Exception as e:
					logger.exception(e)
			elif '0-1:24.2.1' in x:
				try:
					gas_m3 = float(x[28:37])
				except Exception as e:
					logger.exception(e)
			else:
				pass

		self.e_laag_kwh = e_laag_kwh
		self.e_hoog_kwh = e_hoog_kwh
		self.e_huidig_watt = e_huidig_watt
		self.e_huidig_kwh = e_huidig_kwh
		self.gas_m3 = gas_m3

	def print_data(self):
		logger.info("Status")
		logger.info("Timestamp: "+str(datetime.datetime.now()))
		logger.info("#############")
		logger.info('Elektra - Meterstand laag kwh: '+str(self.e_laag_kwh))
		logger.info('Elektra - Meterstand hoog kwh: '+str(self.e_hoog_kwh))
		logger.info('Elektra - Huidig verbruik watt: '+str(self.e_huidig_watt))
		logger.info('Elektra - Huidig verbruik kwh: ' + str(self.e_huidig_kwh))
		logger.info('Gas meterstand m3: '+str(self.gas_m3))

	def store_data(self):

		obs_start=[]
		obs_dict={}

		date_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
		date = datetime.datetime.now().date().strftime("%d-%m-%Y")
		time = datetime.datetime.now().time().strftime("%H:%M:%S")

		obs_dict['date_time'] = date_time
		obs_dict['date'] = date
		obs_dict['time'] = time
		obs_dict['meter_el'] = self.e_laag_kwh
		obs_dict['meter_eh'] = self.e_hoog_kwh
		obs_dict['huidig_e'] = self.e_huidig_watt
		obs_dict['gas'] = self.gas_m3

		obs_start.append(obs_dict)

		if os.path.isfile(self.source_json_path):
			with open(self.source_json_path) as data_file:
				obs = json.load(data_file)

			obs.append(obs_dict)

			with open(self.source_json_path, 'w') as outfile:
				json.dump(obs, outfile)

		else:
			with open(self.source_json_path, 'w') as outfile:
				json.dump(obs_start, outfile)

		logger.info('JSON data stored')


def preprocess_data(raw_data_path, preprocessed_csv_path, price_e, price_g):

	with open(raw_data_path) as data_file:
		obs = json.load(data_file)

	# load data

	df = pd.DataFrame(obs)

	# Electricity; ffil 0 meter readings and calculate consumption  + corresponding costs of consumption

	df['meter_el'] = df['meter_el'].replace(to_replace=0, method='ffill')
	df['el_consumed'] = df['meter_el'].diff()

	df['meter_eh'] = df['meter_eh'].replace(to_replace=0, method='ffill')
	df['eh_consumed'] = df['meter_eh'].diff()

	df['e_total'] = df['eh_consumed']+df['el_consumed']
	df['e_total'] = df['e_total'].astype(float)

	df['e_total_cost'] =  df['e_total'].apply(lambda x: round(x*price_e, 3))

	# Gas; ffil 0 meter readings and calculate consumption  + corresponding costs of consumption

	df['gas'] = df['gas'].replace(to_replace=0, method='ffill')
	df['gas_consumed'] = df['gas'].diff()
	df['gas_consumed'] = df['gas_consumed'].astype(float)

	df['gas_cost'] =  df['gas_consumed'].apply(lambda x: round(x*price_g, 3))

	# Formate date_time, day and hour

	df['date_time'] = pd.to_datetime(df['date_time'], format='%d-%m-%Y %H:%M:%S')
	df['day'] =  df['date_time'].apply(lambda x: x.strftime('%A'))
	df['hour'] =  df['date_time'].apply(lambda x: x.strftime('%H'))

	df.to_csv(preprocessed_csv_path, index=False)

	return df