import logging
import os

from utils import DataFetcher
from utils import preprocess_data

if __name__ == "__main__":

	log_path = "<absolute path to log>"
	source_json_path = "<absolute path to source json>"
	preprocessed_csv_path = "<absolute path to preprocessed data>"

	price_e = 0.42316  #price electricity
	price_g = 1.77187   #price gas

	if os.path.exists(log_path):
		os.remove(log_path)

	logging.basicConfig(level = logging.INFO)

	# Create a logging instance
	logger = logging.getLogger('data_parser')
	logger.setLevel(logging.INFO)

	fh = logging.FileHandler(log_path)
	fh.setLevel(logging.INFO)

	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	fh.setFormatter(formatter)

	logger.addHandler(fh)

	# Fetch data

	data_retriever = DataFetcher(source_json_path)
	data_retriever.fetch_raw_data()
	data_retriever.parse_data()
	data_retriever.store_data()

	preprocessed_data = preprocess_data(source_json_path, preprocessed_csv_path, price_e, price_g)