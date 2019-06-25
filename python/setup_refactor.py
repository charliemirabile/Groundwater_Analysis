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

def get_confirm(name):
    print('Are you sure you want to delete '+name+' forever?')
    return 'y' == input('(Y/n): ')[0].lower()

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

a = {1:True,2:False}
a = editing_menu_with_backup(a,'Pick an option',[('Add 3-True',lambda x: x.update({3:True} or x)),('Toggle 1',lambda x: x.update({1:not x[1]} or x))])
print(a)