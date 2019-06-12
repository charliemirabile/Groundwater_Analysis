import json,os

#thing = open("configuration/config1.json","r")
#print(thing.read())


PATH_TO_CONFIG_FOLDER = 'configuration/'
FILENAME_FOR_ACTIVE_CONFIG = 'active_configuration.txt'


print(os.listdir('configuration'))

def list_of_configurations():
    return [file for file in os.listdir(PATH_TO_CONFIG_FOLDER) if not file == FILENAME_FOR_ACTIVE_CONFIG]

print(list_of_configurations())

#Functions for menu
def new_configuration():
    print("Making a new configuration!\n")
def edit_configuration():
    print("Editing an existing configuration!\n")
def delete_configuration():
    option_dictionary = {}
    for index,value in enumerate(list_of_configurations()):
        option_dictionary[str(index+1)]=value

    if not option_dictionary:
        print('No configurations to select from. Please create at least one first')
        return

    print("\nWhich configuration do you want to delete");
    for index in sorted(option_dictionary):
        print('{0}. {1}'.format(index, option_dictionary[index][0:-5]))

    should_continue = False
    while not should_continue:
        selection = input("Please enter the number corresponding to your selection: ")
        if selection in list(option_dictionary):
            ans = input('Are you sure you want to delete ' + option_dictionary[selection] + ' forever? (Y/n): ')[0].lower()
            if ans == 'y':
                os.remove(PATH_TO_CONFIG_FOLDER + option_dictionary[selection])
                should_continue = True
        else:
            print('Error: Invalid Option')
def set_active():
    option_dictionary = {}
    for index,value in enumerate(list_of_configurations()):
        option_dictionary[str(index+1)]=value

    if not option_dictionary:
        print('No configurations to select from. Please create at least one first')
        return

    print("\nWhich configuration do you want to set active?");
    for index in sorted(option_dictionary):
        print('{0}. {1}'.format(index, option_dictionary[index][0:-5]))

    should_continue = False
    while not should_continue:
        selection = input("Please enter the number corresponding to your selection: ")
        if selection in list(option_dictionary):
            f = open(PATH_TO_CONFIG_FOLDER + FILENAME_FOR_ACTIVE_CONFIG, "w")
            f.write(option_dictionary[selection])
            f.close()
            should_continue = True
        else:
            print('Error: Invalid Option')
#Dictionary mapping
menu_numbers_to_functions = {
    '1': new_configuration,
    '2': edit_configuration,
    '3': delete_configuration,
    '4': set_active
    }


should_continue = False

while not should_continue:
    print('''What would you like to do?
    1. Add a new configuration
    2. Edit an existing configuration
    3. Delete an existing configuration
    4. Set as active configuration''')
    nmbr_selection = input('Please enter the appropriate number to indicate your choice: ')
    if nmbr_selection in menu_numbers_to_functions:
        should_continue=True
        chosen_func = menu_numbers_to_functions[nmbr_selection]
        chosen_func()
    else:
        print('Invalid choice')
