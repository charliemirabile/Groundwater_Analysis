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


#print(pick_config_or_cancel("Which config do you want?"))

def get_confirm(name):
    print('Are you sure you want to delete '+name+' forever?')
    return 'y' == input('(Y/n): ')[0].lower()

#def editing_menu_with_backup(