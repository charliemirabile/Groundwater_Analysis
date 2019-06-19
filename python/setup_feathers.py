import json,os,re
PATH_TO_CONFIG_FOLDER = 'configuration/'
FILENAME_FOR_ACTIVE_CONFIG = 'active_configuration.txt'

def list_of_configurations():
    return [file for file in os.listdir(PATH_TO_CONFIG_FOLDER) if not file == FILENAME_FOR_ACTIVE_CONFIG]

def edit_config_menu(current_config):
    #So far, the edit function here takes a python object that was obtained from JSON
    #The user can edit the object which will the be returned for dumping 
    print(current_config)
    return current_config
    while True:
        print('What would you like to do?\n' +
            '\t1. Cancel\n' + 
            '\t2. Add a new configuration\n' + 
            '\t3. Edit an existing configuration\n' + 
            '\t4. Delete an existing configuration\n' + 
            '\t5. Set as active configuration'
        )
        selection = input('Please enter the appropriate number to indicate your choice: ')
        if selection == '1':
            return
        if selection in top_level_edit_config:
            chosen_func = top_level_edit_config[selection]
            chosen_func()
        else:
            print('-------------------------------------------------------------------')
            print('Invalid choice')    #This function is going to be horible to write because of all the layers too it
    
def get_valid_input(prompt_string):
    response = input(prompt_string)
    while not re.match(r'^([a-zA-Z0-9_\-\(\)])+$', response):
        print("Invalid input, please use only alphanumeric characters undescores dashes or parentheses.")
        response = input(prompt_string)
    return response

def new_configuration():
    option_dictionary = {'1':'Cancel','2':'New empty configuration','3':'Create copy of existing configuration'}
    print('-------------------------------------------------------------------')
    print("What do you want to do?");
    for index in sorted(option_dictionary):
        print('{0}. {1}'.format(index, option_dictionary[index]))
    selection = input('Please enter the appropriate number to indicate your choice: ')
    if selection == '1':
        print('-------------------------------------------------------------------')
        return
    if selection == '2':
        print('-------------------------------------------------------------------')
        print('What should the new configuration be named?')
        name = get_valid_input('Name: ')
        f = open(PATH_TO_CONFIG_FOLDER + name + '.json','w')
        json.dump(edit_config_menu({}),f, indent=2)
        f.close()
        return
    if selection == '3':
        config_dictionary = {}
        for index,value in enumerate(list_of_configurations()):
            config_dictionary[str(index+1)]=value[0:-5]
        print('-------------------------------------------------------------------')
        print('What configuration do you want to copy?')
        for index in sorted(config_dictionary):
            print('\t{0}. {1}'.format(index, config_dictionary[index]))
        while True:        
            selection = input("Please enter the number corresponding to your selection: ")
            if selection in list(config_dictionary):
                print('What should the new configuration be named?')
                name = get_valid_input('Name: ')
                original = open(PATH_TO_CONFIG_FOLDER + config_dictionary[selection] + '.json','r')
                copy = open(PATH_TO_CONFIG_FOLDER + name + '.json','w')
                json.dump(json.load(original),copy, indent=2)
                original.close()
                copy.close()
                return
            print('-------------------------------------------------------------------')
            print('Error: Invalid Option')
            print("Which configuration do you want to delete");    
        
    
def edit_configuration():
    option_dictionary = {'1':'Cancel'}
    for index,value in enumerate(list_of_configurations()):
        option_dictionary[str(index+2)]=value[0:-5]
    print('-------------------------------------------------------------------')
    print("Which configuration do you want to edit");
    for index in sorted(option_dictionary):
        print('{0}. {1}'.format(index, option_dictionary[index]))
    
    while True:
        selection = input("Please enter the number corresponding to your selection: ")
        if(selection == '1'):
            print('-------------------------------------------------------------------')
            return
        if selection in list(option_dictionary):
            with open(PATH_TO_CONFIG_FOLDER + option_dictionary[selection]+'.json') as f:
                current = json.load(f)
            edit_config_menu(current)
            return
        else:
            print('Error: Invalid Option')
            
def delete_configuration():
    option_dictionary = {'1':'Cancel'}
    for index,value in enumerate(list_of_configurations()):
        option_dictionary[str(index+2)]=value[0:-5]

    print('-------------------------------------------------------------------')
    print("Which configuration do you want to delete");
    for index in sorted(option_dictionary):
        print('\t{0}. {1}'.format(index, option_dictionary[index]))
    while True:        
        selection = input("Please enter the number corresponding to your selection: ")
        if(selection == '1'):
            print('-------------------------------------------------------------------')
            return
        if selection in list(option_dictionary):
            ans_string = input('Are you sure you want to delete ' + option_dictionary[selection] + ' forever? (Y/n): ')
            ans = ans_string[0].lower()
            if ans == 'y':
                os.remove(PATH_TO_CONFIG_FOLDER + option_dictionary[selection] + '.json')
                print('-------------------------------------------------------------------')
                print('Successfully deleted ' + option_dictionary[selection])
            else:
                print('-------------------------------------------------------------------')
                print('Deletion cancelled')
            return
        print('-------------------------------------------------------------------')
        print('Error: Invalid Option')
        print("Which configuration do you want to delete");
        for index in sorted(option_dictionary):
            print('\t{0}. {1}'.format(index, option_dictionary[index]))
def set_active():
    option_dictionary = {'1':'Cancel'}
    for index,value in enumerate(list_of_configurations()):
        option_dictionary[str(index+2)]=value[0:-5]

    print('-------------------------------------------------------------------')
    print('Which configuration do you want to set active?')
    for index in sorted(option_dictionary):
        print('\t{0}. {1}'.format(index, option_dictionary[index]))

    while True:
        selection = input("Please enter the number corresponding to your selection: ")
        if selection == '1':
            print('-------------------------------------------------------------------')
            return
        if selection in list(option_dictionary):
            f = open(PATH_TO_CONFIG_FOLDER + FILENAME_FOR_ACTIVE_CONFIG, "w")
            f.write(option_dictionary[selection])
            f.close()
            print('-------------------------------------------------------------------')
            print('Successfully set ' + option_dictionary[selection] + 'as active configuration')
            return
        print('-------------------------------------------------------------------')
        print('Error: Invalid Option')
        print('Which configuration do you want to set active?')
        for index in sorted(option_dictionary):
            print('\t{0}. {1}'.format(index, option_dictionary[index]))

menu_numbers_to_functions = {
    '2': new_configuration,
    '3': edit_configuration,
    '4': delete_configuration,
    '5': set_active
    }

def main_menu():
    while True:
        print('What would you like to do?\n' +
            '\t1. Cancel\n' + 
            '\t2. Add a new configuration\n' + 
            '\t3. Edit an existing configuration\n' + 
            '\t4. Delete an existing configuration\n' + 
            '\t5. Set as active configuration'
        )
        selection = input('Please enter the appropriate number to indicate your choice: ')
        if selection == '1':
            return
        if selection in menu_numbers_to_functions:
            chosen_func = menu_numbers_to_functions[selection]
            chosen_func()
        else:
            print('-------------------------------------------------------------------')
            print('Invalid choice')

main_menu()