import json

should_continue = False

while should_continue == False:
	print('''What would you like to do?
	1. Read in and modify existing feather configuration
	2. Start new feather configuration and overwrite previous''')
	line = input('Please enter the appropriate number to indicate your choice:')
	if not (len(line) == 1):
		print('bad')
