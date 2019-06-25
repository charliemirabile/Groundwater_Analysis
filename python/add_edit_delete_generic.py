#This file contains functions that will act as generic helpers to the menu system


#Pre: sub_dictionary is a valid subdict of the current configuration that is being modified, type is a valid string
#Post: sub_dictionary has a new key value pair and is returned to the caller
def generic_add(sub_dictionary, type):
	key = get_regex_input(r'^([a-zA-Z0-9_\-\(\)])+$',
				'Please enter a new' + type + 'key: ',
				'Invalid input, please enter only alphanumeric characters underscores dashes or parthesis')
	value = get_regex_input(r'^([0-9])+$',
				'Please enter the value for' + type + ': ',
				'Invalid input, please enter only numeric characters')
	sub_dictionary[key] = value
	return sub_dictionary

def generic_delete(sub_dictionary, type):
	
