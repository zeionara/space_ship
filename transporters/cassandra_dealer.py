import sys, os, datetime
from bson.objectid import ObjectId
import configparser

config = configparser.ConfigParser()
config.read(os.environ.get('SPACE_SHIP_HOME') + '/databases.config')

TIMESTAMP_PATTERN = os.environ.get('TIMESTAMP_PATTERN') or config['FORMATS']['timestamp']
TIME_PATTERN = os.environ.get('TIME_PATTERN') or config['FORMATS']['time']
DATE_PATTERN = os.environ.get('DATE_PATTERN') or config['FORMATS']['date']

## Convert stringified list back to list 
def string_to_list(strlist):
	return [float(item.lstrip().rstrip()) for item in strlist.replace('[','').replace(']','').split(',')]

## Convert item's property from mongo format to cassandra query format
def stringify(value):
	if isinstance(value, datetime.datetime):
		return '\'' + value.strftime(TIMESTAMP_PATTERN) + '\''
	elif isinstance(value, list):
		return '\'' + str(value) + '\''
	elif isinstance(value, int) or isinstance(value, float):
		return str(value)
	elif isinstance(value, ObjectId):
		return '0x' + str(value)
	return '\'' + str(value) + '\''

## Convert item from mongo format to cassandra query format
def querify(item, mode = 'INSERT'):
	querified = []
	for key in item:
		if item[key]:
			try:
				if key.index('__') == 0:
					querified.append([key[2:], stringify(item[key])])
			except:
				try:
					if key.index('_') == 0:
						querified.append([key[1:], stringify(item[key])])
				except:
					querified.append([key, stringify(item[key])])
					continue

	if mode == 'INSERT':
		return '(' + ', '.join([item[0] for item in querified]) + ') values (' + ', '.join([item[1] for item in querified]) + ')'
	elif mode == 'SELECT':
		criterias = [item[0] + ' = ' + item[1] for item in querified]
		joined_criterias = ', '.join(criterias)
		return 'where {0} allow filtering'.format(joined_criterias) if (len(criterias) > 0) else joined_criterias

## Convert item, came from cassandra, to mongo format
def repair(item):
	repaired = {}
	for key in item:
		if key == 'cause__':
			continue
		elif key == 'gaps__':
			repaired['__' + key] = string_to_list(item[key])
		else:
			try:
				if key.index('__') == len(key) - 2:
					repaired['__' + key] = item[key]
			except:
				if key == 'id':
					repaired['_' + key] = ObjectId(item[key])
				else:
					repaired[key] = item[key]

	return repaired