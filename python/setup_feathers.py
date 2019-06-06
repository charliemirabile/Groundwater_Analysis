import json,os

thing = open("configuration/config1.json","r")
print(thing.read())

#Functions for menu
def newConfiguration():
    print("Making a new configuration!\n")
def editConfiguration():
    print("Editing an existing configuration!\n")
def deleteConfiguration():
    print("Deleting an existing configuration!\n")
def setActive():
    print("Setting a new active configuration!\n")

#Dictionary mapping
MenuSelect = {
    1: newConfiguration,
    2: editConfiguration,
    3: deleteConfiguration,
    4: setActive
    }


should_continue = False

while should_continue == False:
    print('''What would you like to do?
    1. Add a new configuration
    2. Edit an existing configuration
    3. Delete an existing configuration
    4. Set as active configuration''')
    selection = int(input('Please enter the appropriate number to indicate your choice:'))

    if (selection <= 0) or (selection > 4):
        should_continue = False
    else:
        MenuSelect[selection]()
        should_continue = True
	
	
