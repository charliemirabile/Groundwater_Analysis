import json, os, re

def get_valid_input(prompt_string):
	response = input(prompt_string)
	while not re.match(r'^([a-zA-Z0-9_\-\(\)])+$', response):
		print("Invalid input, please use only alphanumeric characters undescores dashes or parentheses.")
		response = input(prompt_string)
	return response

def edit_node_level_identifiers(current_config):
	backup_config = current_config
	option_dictionary = {'1':'Cancel', '2':'Save and return to previos menu', '3': 'Create new node identifier', '4': 'Edit existing node identifier',
	{'5': 'Delete existing node identifier'}
	print("What do you want to do?")
	return current_config

def edit_field_identifiers(current_config):
	backup_config = current_config
	if 'field_identifiers' not in current_config['iSense_info']:
		current_config['iSense_info']['field_identifiers'] = {}
	option_dictionary = {'1':'Cancel', '2' : 'Save and return to previous menu', '3': 'Edit timestamp identifier', '4' : 'Edit reading identifier',
	'5': 'Edit node level identifiers', '6': 'Edit sesor level identifiers'}
	print("What do you want to do?")
	print('-------------------------------------------------------------------')
	while True:
		for index in sorted(option_dictionary):
			print('{0}. {1}'.format(index, option_dictionary[index]))
		selection = input("Please enter the appropriate number to indicate your choice: ")
		if selection == '1':
			print('-------------------------------------------------------------------')
			print('Successfully canceled changes')
			return backup_config
		if selection == '2':
			print('-------------------------------------------------------------------')
			print('Successfully saved changes')
			return current_config
		if selection == '3':
			timestamp_identifier = get_valid_input("Please enter the timestamp identifier: ")
			current_config['iSense_info']['field_identifiers']['timestamp_identifier'] = timestamp_identifier
			print('-------------------------------------------------------------------')
			print('Successfully changed the timestamp identifier')
		if selection == '4':
			reading_identifier = get_valid_input("Please enter the reading identifier: ")
			current_config['iSense_info']['field_identifiers']['reading_identifier'] = reading_identifier
		if selection == '5':
			edit_node_level_identifiers()
		if selection == '6':
			edit_sensor_level_identifiers()
def edit_iSense_config(current_config):
	backup_config = current_config
	if 'iSense_info' not in current_config:
		current_config['iSense_info'] = {}
	option_dictionary = {'1':'Cancel', '2': 'Save and return to previous menu',  '3': 'Edit dataset ID', '4':'Edit contribution key', '5': 'Edit field identifiers'}
	print("What do you want to do?")
	print('-------------------------------------------------------------------')
	while True:
		for index in sorted(option_dictionary):
			print('{0}. {1}'.format(index, option_dictionary[index]))
		selection = input("Please enter the appropriate number to indicate your choice: ")
		if selection == '1':
			print('-------------------------------------------------------------------')
			print('Successfully canceled changes')
			return backup_config
		if selection == '2':
			print('-------------------------------------------------------------------')
			print('Successfully saved changes')
			return current_config
		if selection == '3':
			dataset_id =  get_valid_input("Please enter the iSense dataset ID: ")
			current_config['iSense_info']['dataset_id'] = dataset_id
			print('-------------------------------------------------------------------')
			print("Successfully changed the dataset ID")
		if selection == '4':
			contribution_key = get_valid_input("Please enter the iSense contribution key: ")
			current_config['iSense_info']['contribuition_key'] = contribution_key
			print('-------------------------------------------------------------------')
			print("Successfully changed the contribution_key")
		if selection == '5':
			edit_field_identifiers(current_config)
test = {}
edit_iSense_config(test)
