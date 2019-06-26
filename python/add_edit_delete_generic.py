#This file contains functions that will act as generic helpers to the menu system


#Pre: sub_dictionary is a valid subdict of the current configuration that is being modified, type is a valid string
#Post: sub_dictionary has a new key value pair and is returned to the caller
def generic_add(sub_dictionary, type):
	key = get_regex_input(r'^([a-zA-Z0-9_\-\(\)])+$',
				'Please enter a new' + type + 'key: ',
				'Invalid input, please enter only alphanumeric characters underscores dashes or parenthesis')
	value = get_regex_input(r'^([0-9])+$',
				'Please enter the value for' + type + ': ',
				'Invalid input, please enter only numeric characters')
	sub_dictionary[key] = value
	return sub_dictionary


def generic_delete(sub_dictionary, name):
	if(get_confirm("Are you sure you want to delete " + name + "?")):
		del sub_dictionary[name]
		print('Successfully deleted ' + name)
		return
	print('Deletion canceled')
	return


def generic_edit(sub_dictionary, name):
	value = get_regex_input(r'^([a-zA-Z0-9_\-\(\)])+$',
				'Please enter the new value for ' + name + ': ',
				'Invalid input, please enter only alphanumeric characters underscores dashes or parenthesis'')
	sub_dictionary[name] = value
