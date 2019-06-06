import serial,requests,json,time,datetime,sys

base_station_feather_identifier = '/dev/ttyACM0'

feather_ids_to_address_dictionaries_for_descriptions = {
	'1337':
	{
		'100':"battery",
		'69':"temperature",
		'102':"banana"
	},
	'1338':
	{
		'100':"battery",
		'101':"test"
	}
}

node_ids_to_position_information = {
	'1337':
	{
		"depth":'5',
		"lat":'5',
		"long":'5'
	},
	'1338':
	{
		"depth":'7',
		"lat":'8',
		"long":'3'
	}
}


iSense_field_idenfifiers = {#MUST ADD

	'timestamp' : '18367',
	'metric' : '18370',
	'latitude' : '18365',
	'longitude' : '18366',
	'depth' : '18368',
	'reading' : '18369'
}




iSense_contribution_key = 'keykey'

iSense_dataset_id = 101111

def get_formatted_timestamp():
	return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

def iSense_append_data(contribution_key,dataset_ID,data):
	payload = {
		'contribution_key':contribution_key,
		'id':dataset_ID,
		'data':data
	}
	print(data['18370'])
	headers = {'content-type':'application/json'}
	request = requests.post('https://isenseproject.org/api/v1/data_sets/append',data=json.dumps(payload),headers=headers)
	print(request)
	print(request.text)
#	request.text

try:
	base_station_feather = serial.Serial(base_station_feather_identifier,9600)
except KeyboardInterrupt as e:
	raise
except:
	e = sys.exc_info()[0]
	print(e)
	print('unable to connect with base station feather - device not found at specified address')
	raise

while True:
	try:
		input = str(base_station_feather.readline())

		print(input)

		try:
			feather_identifier, sensor_identifier, reading = input.split(':')
		except ValueError as e:
			print(e)
			print('malformed message - wrong number of delimeters')
		try:
			print(sensor_identifier)
			data = {
				iSense_field_idenfifiers['timestamp']:[get_formatted_timestamp()],
				iSense_field_idenfifiers['latitude']:[node_ids_to_position_information[feather_identifier]['lat']],
				iSense_field_idenfifiers['longitude']:[node_ids_to_position_information[feather_identifier]['long']],
				iSense_field_idenfifiers['depth']:[node_ids_to_position_information[feather_identifier]['depth']],
				iSense_field_idenfifiers['reading']:[reading],
				iSense_field_idenfifiers['metric']:[feather_ids_to_address_dictionaries_for_descriptions[feather_identifier][sensor_identifier]]
				}
		except KeyError as e:
			print(e)
			print('unexpected sensor identifier encountered - no corresponding feild in iSense')
			raise
	except NameError as e:
		print(e)
		print('here')
		raise
		try:
			iSense_append_data(iSense_contribution_key,iSense_dataset_id,data)
		except requests.exceptions.RequestException as e:
			print(e)
			print('error making request to iSense - no internet or issues with iSense')
		raise
	except KeyboardInterrupt as e:
		raise
	except:
		e = sys.exc_info()[0]
		print(e)
