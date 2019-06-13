import json,os

PATH_TO_CONFIG_FOLDER = 'configuration/'
FILENAME_FOR_ACTIVE_CONFIG = 'active_configuration.txt'

def list_of_configurations():
    return [file for file in os.listdir(PATH_TO_CONFIG_FOLDER) if not file == FILENAME_FOR_ACTIVE_CONFIG]

def edit_config_menu(current_config):
    return current_config

#Functions for menu
def new_configuration():
    print("Making a new configuration!\n")
def edit_configuration():
    option_dictionary = {'1':'Cancel'}
    for index,value in enumerate(list_of_configurations()):
        option_dictionary[str(index+2)]=value[0:-5]
    print('-------------------------------------------------------------------')
    print("Which configuration do you want to edit");
    for index in sorted(option_dictionary):
        print('{0}. {1}'.format(index, option_dictionary[index]))
    
    should_continue = False
    while not should_continue:
        selection = input("Please enter the number corresponding to your selection: ")
        if(selection == '1'):
            print('-------------------------------------------------------------------')
            return
        if selection in list(option_dictionary):
            ans = input('Are you sure you want to delete ' + option_dictionary[selection] + ' forever? (Y/n): ')[0].lower()
            if ans == 'y':
                os.remove(PATH_TO_CONFIG_FOLDER + option_dictionary[selection] + '.json')
                should_continue = True
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

#Dictionary mapping
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