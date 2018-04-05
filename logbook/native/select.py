import sys, os
import math
import configparser
import numpy as np
import operator

sys.path.append('entities')

from cassandra.cqlengine import connection

from position import Position
from system_test import SystemTest

config = configparser.ConfigParser()
config.read('../databases.config')

DB_URL = os.environ.get('DB_URL') if os.environ.get('DB_URL') else config['CASSANDRA']['host']
DB_NAME = os.environ.get('DB_NAME') if os.environ.get('DB_NAME') else config['CASSANDRA']['db_name']

def select(table_name, columns):
	columns_filter = ', '.join([item[0] for item in columns])
	values_filter = ' and '.join([\
		item[0] + ' = ' + str(item[1])\
		if isinstance(item[1], int) or isinstance(item[1], float) else\
		item[0] + ' = \'' + str(item[1]) + '\'' \
		for item in (item for item in columns if len(item) > 1)\
	])

	if len(values_filter) > 0:
		values_filter = 'where ' + values_filter
	print('select {2} from {0}.{1} {3} allow filtering;'.format(DB_NAME, table_name, columns_filter, values_filter))
	return connection.execute('select {2} from {0}.{1} {3} allow filtering;'.format(DB_NAME, table_name, columns_filter, values_filter)).current_rows

def main():
	connection.setup([DB_URL], DB_NAME)

	table_name = sys.argv[1]
	columns = [column.split('=') for column in sys.argv[2:]]

	print(select(table_name, columns))

	select('position', [['x', 10], ['y', 10], ['speed'], ['time']])

if __name__ == '__main__':
	main()