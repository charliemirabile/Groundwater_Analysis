#This file contains functions that will act as generic helpers to the menu system

def generic_add(sub_dictionary, type):
	key = get_regex_input(r'^([a-zA-Z0-9_\-\(\)])+$',
				'Please enter a new' + type + 'key: ',
				'Invalid input, please enter only alphanumeric characters underscores dashes or parthesis')
	value = get_regex_input(r'^([0-9])+$',
				'Please enter the value for' + type + ': ',
				'Invalid input, please enter only numeric characters')
	sub_dictionary[key] = value

def generic_delete(sub_dictionary, type):
	
