
import json, os

def check_json (json_object):
	result = True
	node_level_identifiers = []
	sensor_level_identifiers = []
#iSense portion check
	if 'iSense_info' in json_object:
		if 'dataset_id' not in json_object['iSense_info']:
			print('Invalid configuration - no dataset id')
			result = False
		if 'contribution_key' not in json_object['iSense_info']:
			print('Invalid configuration - no contribution key')
			result = False
		if 'field_identifiers' in json_object['iSense_info']:
			if 'timestamp_identifier' not in json_object['iSense_info']['field_identifiers']:
				print('Invalid configuration - no timestamp identifier')
				result = False
			if 'reading_identifier' not in json_object['iSense_info']['field_identifiers']:
				print('Invalid configuration - no reading identifier')
				result = False
			if 'node_level' in json_object['iSense_info']['field_identifiers']:
				for data in json_object['iSense_info']['field_identifiers']['node_level']:
					node_level_identifiers.append(data)
			if 'sensor_level' in json_object['iSense_info']['field_identifiers']:
				for data in json_object['iSense_info']['field_identifiers']['sensor_level']:
					sensor_level_identifiers.append(data)
		else:
			print('Invalid configuration - no field identifiers')
			result = False
	else:
		print('Invalid configuration - no iSense info')
		result = False

#node portion check
	if 'nodes' in json_object:
		for node in json_object['nodes']:
		#Checking if the node level identifiers match the iSense info
			for identifier_check in node_level_identifiers:
				if identifier_check not in json_object['nodes'][node]['node_level']:
					print('Invalid configuration - missing node level idenetifier in the node '+node)
					result = False
		#Checking if the sensor level identifiers match the iSense info
			for identifier_check in sensor_level_identifiers:
				if identifier_check not in json_object['nodes'][node]['sensor_level']:
					print('Invalid configuration - missing sesnor level identifier in the node '+node)
					result = False
	else:
		print('Invalid configuration - no nodes detected')
		result = False
	print('returning result as - '+ str(result))
	return result

