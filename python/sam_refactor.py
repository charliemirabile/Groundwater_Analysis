import json,os,re
PATH_TO_CONFIG_FOLDER = 'configuration/'
FILENAME_FOR_ACTIVE_CONFIG = 'active_configuration.txt'

def pick_config_or_cancel(prompt_string):
	list_of_configs = [file_name for file_name in os.listdir(PATH_TO_CONFIG_FOLDER) if not file_name == FILENAME_FOR_ACTIVE_CONFIG]
	print('-------------------------------------------------------------------')
	while True:
		print(prompt_string)
		print('1. Cancel')
		valid_choices = set()
		for index,name in enumerate(list_of_configs):
			valid_choices.add(str(index+2))
			print("{0}. {1}".format(index+2,name[:-5]))
		choice = input('Enter the number corresponding to your selection: ')
		if choice == '1': return 'Cancel'
		if choice in valid_choices: return list_of_configs[int(choice)-2]
		print('-------------------------------------------------------------------')
		print("Error, invalid input.")



def pick_subdict_or_cancel(subdict, prompt_string):
	list_of_keys = list(subdict.keys())
	valid_choices = set()
	for index,name in enumerate(list_of_keys):
		valid_choices.add(str(index+2))
	print('-------------------------------------------------------------------')
	while True:
		print(prompt_string)
		print('1. Cancel')
		for index,name in enumerate(list_of_keys):
			print("{0}. {1}".format(index+2,name))
		choice = input('Enter the number corresponding to your selection: ')
		if choice == '1': return 'Cancel'
		if choice in valid_choices: return list_of_keys[int(choice)-2]
		print('-------------------------------------------------------------------')
		print("Error, invalid input.")


#print(pick_subdict_or_cancel({1:True,2:False},"Which cuh do you want?"))

def get_confirmation(message):
	print(message)
	return 'y' == input('(Y/n): ')[0].lower()

def get_regex_input(regex, prompt_string, error_string):
	response = input(prompt_string)
	while not re.match(regex, response):
		print(error_string)
		response = input(prompt_string)
	return response

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
				'Invalid input, please enter only alphanumeric characters underscores dashes or parenthesis')
	sub_dictionary[name] = value

def editing_menu_with_backup(subdictionary,prompt_string,options_list):
	backup = json.loads(json.dumps(subdictionary))
	valid_choices = set()
	for index,name in enumerate(options_list):
		valid_choices.add(str(index+3))
	print('-------------------------------------------------------------------')
	while True:
		print(prompt_string)
		print('1. Cancel and return to previous menu')
		print('2. Save and return to previous menu')
		for index,value in enumerate(options_list):
			print('{0}. {1}'.format(index+3,value[0]))
		choice = input('Enter the number corresponding to your selection: ')
		if choice == '1': return backup
		if choice == '2': return subdictionary
		if choice in valid_choices:
			options_list[int(choice)-3][1](subdictionary)
			print('-------------------------------------------------------------------')
			continue
		print('-------------------------------------------------------------------')
		print('Error, invalid input')

#a = {1:True,2:False}
#a = editing_menu_with_backup(a,'Pick an option',[('Add 3-True',lambda x: x.update({3:True} or x)),('Toggle 1',lambda x: x.update({1:not x[1]} or x))])
#print(a)



def basic_selection_menu(prompt_string,options_list):
	valid_choices = set()
	for index,name in enumerate(options_list):
		valid_choices.add(str(index+2))
	print('-------------------------------------------------------------------')
	while True:
		print(prompt_string)
		print('1. Cancel')
		for index,value in enumerate(options_list):
			print('{0}. {1}'.format(index+2,value[0]))
		choice = input('Enter the number corresponding to your selection: ')
		if choice == '1': return 'cancel'
		if choice in valid_choices:
			print('-------------------------------------------------------------------')
			return options_list[int(choice)-2][1]
		print('-------------------------------------------------------------------')
		print('Error, invalid input')






#def new_configuration():print('-------------------------------------------------------------------');print('new')
#def edit_configuration():print('-------------------------------------------------------------------');print('edit')
#def delete_configuration():print('-------------------------------------------------------------------');print('delete')
#def set_active():print('-------------------------------------------------------------------');print('active')

def setup_sub_dictionary_and_call(top_dict,name_of_sub, func):
	if name_of_sub not in top_dict:
		top_dict[name_of_sub]={}
	return func(top_dict[name_of_sub])

def add_edit_delete_generic

def edit_field_identifiers(subdict):
	subdict = editing_menu_with_backup(subdict,
							'What do you want to edit',
							[('Edit timestamp identifier', lambda x: generic_edit(x, 'timestamp_identifier')),
							 ('Edit reading identifier', lambda x: generic_edit(x , 'reading_identifier'))])

def edit_iSense_info(subdict):
	subdict = editing_menu_with_backup(subdict, 
							'What do you want to edit?',
							[('Edit dataset id', lambda x: generic_edit(x, 'dataset_id')),
							 ('Edit contribution key', lambda x: generic_edit(x, 'contribution_key')),
							 ('Edit field identifiers', lambda x: setup_sub_dictionary_and_call(x, 'field_identifiers', edit_field_identifiers))])
	print(subdict)
	
def edit_node_info(subdict):
	print('foof')
	print(subdict)
	
def edit_configuration():
	choice = pick_config_or_cancel('Which configuration do you want to edit?')
	if choice == 'cancel':print('-------------------------------------------------------------------');return
	file = open(PATH_TO_CONFIG_FOLDER + choice,'r')
	current_config = json.load(file)
	file.close()
	current_config = editing_menu_with_backup(current_config,
										 'What do you want to edit?',
										 [('Edit iSENSE info',lambda x: setup_sub_dictionary_and_call(x,'iSense_info',edit_iSense_info)),
										  ('Edit node info', lambda x: setup_sub_dictionary_and_call(x,'nodes',edit_node_info))])
	file = open(PATH_TO_CONFIG_FOLDER + choice,'w')
	json.dump(current_config,file,indent=2)
	file.close()

def new_configuration():
	choice = basic_selection_menu('What would you like to do?',
								  [('Create new empty configuration','empty'),
								   ('Create copy of existing configuration','copy')])
	if choice == 'cancel':print('-------------------------------------------------------------------');return
	
	name = get_regex_input(r'^([a-zA-Z0-9_\-\(\)])+$',
							   'What should the configuration be named: ',
							   'Error, name may only contain letters numbers underscores or parentheses')
	if choice == 'empty':
		f = open(PATH_TO_CONFIG_FOLDER + name + '.json','w')
		f.write('{}')
		f.close()
		print('-------------------------------------------------------------------')
		print('Successfully added new configuration ' + name)
		return
	if choice == 'copy':
		selection = pick_config_or_cancel('Which config do you want to copy?')
		if selection == 'cancel':
			return
		original = open(PATH_TO_CONFIG_FOLDER + selection,'r')
		copy = open(PATH_TO_CONFIG_FOLDER + name + '.json','w')
		json.dump(json.load(original),copy, indent=2)
		original.close()
		copy.close()
		print('-------------------------------------------------------------------')
		print('Successfully added new configuration ' + name)
		return
		

def delete_configuration():
	print('-------------------------------------------------------------------')
	choice = pick_config_or_cancel('Which configuration do you want to delete?')
	if choice == 'Cancel':
		print('-------------------------------------------------------------------')
		return
	f = open(PATH_TO_CONFIG_FOLDER + FILENAME_FOR_ACTIVE_CONFIG, 'r')
	line = f.read()
	f.close()
	if line==choice:
		print('-------------------------------------------------------------------')
		print('Cannot delete active configuration. Deletion cancelled')
		return
	if get_confirmation('Are you sure you want to delete '+choice[:-5]+' forever?'):
		os.remove(PATH_TO_CONFIG_FOLDER+choice)
		print('-------------------------------------------------------------------')
		print('Successfully deleted '+choice[:-5])
	else:
		print('-------------------------------------------------------------------')
		print('Deletion cancelled')


def set_active():
	print('-------------------------------------------------------------------')
	choice = pick_config_or_cancel('Which configuration do you want to set active?')
	if choice == 'Cancel':
		print('-------------------------------------------------------------------')
		return
	f = open(PATH_TO_CONFIG_FOLDER + FILENAME_FOR_ACTIVE_CONFIG, 'w')
	f.write(choice)
	f.close()
	print('-------------------------------------------------------------------')
	print('Successfully set '+choice[:-5]+' as active configuration')


def main_menu():
	option_dictionary = {'1':'Cancel','2':'Add new configuration','3':'Edit configuration','4':'Delete configuration','5':'Set the active configuration'}
	print('-------------------------------------------------------------------')
	while True:
		print('What would you like to do?')
		for index in sorted(option_dictionary):
			print('{0}. {1}'.format(index, option_dictionary[index]))
		selection = input('Please enter the appropriate number to indicate your choice: ')
		if selection == '1':
			print('-------------------------------------------------------------------')
			return
		if selection == '2':
			new_configuration()
			continue
		if selection == '3':
			edit_configuration()
			continue
		if selection == '4':
			delete_configuration()
			continue
		if selection == '5':
			set_active()
			continue
		print('-------------------------------------------------------------------')
		print('Invalid choice')

main_menu()
