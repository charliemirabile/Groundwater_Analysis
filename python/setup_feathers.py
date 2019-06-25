import json,os,re
PATH_TO_CONFIG_FOLDER = 'configuration/'
FILENAME_FOR_ACTIVE_CONFIG = 'active_configuration.txt'

def list_of_configurations():
    return [file for file in os.listdir(PATH_TO_CONFIG_FOLDER) if not file == FILENAME_FOR_ACTIVE_CONFIG]

def get_valid_input(prompt_string):
    response = input(prompt_string)
    while not re.match(r'^([a-zA-Z0-9_\-\(\)])+$', response):
        print("Invalid input, please use only alphanumeric characters undescores dashes or parentheses.")
        response = input(prompt_string)
    return response

def edit_iSense_config(current_config):
    print('-------------------------------------------------------------------')
    print('edited iSense info')
    print('-------------------------------------------------------------------')
    return current_config

def edit_node_config(current_config):
    print('-------------------------------------------------------------------')
    print('edited node info')
    print('-------------------------------------------------------------------')
    return current_config

def edit_config_menu(current_config):
    backup_config = current_config
    #So far, the edit function here takes a python object that was obtained from JSON
    #The user can edit the object which will the be returned for dumping
    while True:
        print('-------------------------------------------------------------------')
        option_dictionary = {'1': 'Cancel', '2':'Save and return to previous menu', '3':'Edit iSense configuration', '4':'Edit Nodes'}
        print("What do you want to do?")
        for index in sorted(option_dictionary):
            print('{0}. {1}'.format(index, option_dictionary[index]))
        selection = input('Please enter the appropriate number to indicate your choice: ')
        if selection=='1':
            print('-------------------------------------------------------------------')
            print('Successfully cancelled changes')
            return backup_config
        if selection=='2':
            print('-------------------------------------------------------------------')
            print('Successfully saved changes')
            return current_config
        if selection=='3':
            current_config = edit_iSense_config(current_config)
            continue
        if selection=='4':
            current_config = edit_node_config(current_config)
            continue
        print('Error invalid choice')
    
    return current_config

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
        f.write('{}')
        f.close()
        print('-------------------------------------------------------------------')
        print('Successfully added new configuration' + name)
        return
    if selection == '3':
        config_dictionary = {}
        for index,value in enumerate(list_of_configurations()):
            config_dictionary[str(index+1)]=value[0:-5]
        print('-------------------------------------------------------------------')
        print('What configuration do you want to copy?')
        for index in sorted(config_dictionary):
            print('{0}. {1}'.format(index, config_dictionary[index]))
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
                print('-------------------------------------------------------------------')
                print('Successfully added new configuration' + name)
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
        print('{0}. {1}'.format(index, option_dictionary[index]))
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
            print('{0}. {1}'.format(index, option_dictionary[index]))
def set_active():
    option_dictionary = {'1':'Cancel'}
    for index,value in enumerate(list_of_configurations()):
        option_dictionary[str(index+2)]=value[0:-5]

    print('-------------------------------------------------------------------')
    print('Which configuration do you want to set active?')
    for index in sorted(option_dictionary):
        print('{0}. {1}'.format(index, option_dictionary[index]))

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
            print('Successfully set ' + option_dictionary[selection] + ' as active configuration')
            return
        print('-------------------------------------------------------------------')
        print('Error: Invalid Option')
        print('Which configuration do you want to set active?')
        for index in sorted(option_dictionary):
            print('\t{0}. {1}'.format(index, option_dictionary[index]))

def main_menu():
    option_dictionary = {'1':'Cancel','2':'Add new configuration','3':'Edit configuration','4':'Delete configuration','5':'Set the active configuration'}
    print('-------------------------------------------------------------------')
    while True:
        print('What would you like to do?')
        for index in sorted(option_dictionary):
            print('{0}. {1}'.format(index, option_dictionary[index]))
        selection = input('Please enter the appropriate number to indicate your choice: ')
        if selection == '1':
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