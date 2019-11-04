import serial,requests,json,time,datetime,sys
print('oof1')
def append(data):
    payload = {
        'contribution_key':contribution_key,
        'id':dataset_ID,
        'data':data
    }
    headers = {'content-type':'application/json'}
    request = requests.post('https://isenseproject.org/api/v1/data_sets/append',data=json.dumps(payload),headers=headers)
    json.loads(request.text)
    #print(request)
    #print(request.url)
    #print(request.text)

def current_timestamp():
    currentTime = time.time()
    formattedTime = datetime.datetime.fromtimestamp(currentTime).strftime('%Y-%m-%d %H:%M:%S')
    return formattedTime


def init_new_dataset():
    payload = {
        'title': dataset_base_name+datetime.datetime.fromtimestamp(time.time()).strftime('_%Y_%m_%d_%H_%M_%S'),
        'contribution_key': contribution_key,
        'contributor_name': contributor_name,
        'data':{#garbage placeholder data since you cannot create an empty dataset >:(
            latitude_ID:['0'],
            longitude_ID:['0'],
            timestamp_ID:[current_timestamp()],
            reading_ID:['-1'],
            depth_ID:['-1'],
            type_ID:['NULL']
        }
    }
    print(payload)
    headers = {'content-type':'application/json'}
    url = 'https://isenseproject.org/api/v1/projects/'+project_ID+'/jsonDataUpload'
    print(url)
    request = requests.post(url,data=json.dumps(payload),headers=headers)
    #print(request)
    #print(request.url)
    #print(request.text)
    request_json=json.loads(request.text)
    print(request)
    newid = request_json['id']
    print('Switching to dataset with id: ',newid)
    return newid



feather_ids_to_address_dictionaries_for_descriptions = {
	'1337':
	{
		'7':'battery',
		'20':'temperature1',
		'21':'conductivity1',
                '30':'temperature2',
                '31':'conductivity2'
	}
}

node_ids_to_position_information = {
	'1337':
	{
		'depth':'5',
		'lat':'5',
		'long':'5'
	}
}

dataset_base_name = 'BoatHouseTest'
contribution_key = 'python'
contributor_name = 'Raspberry Pi'
dataset_limit = 15
project_ID = '3744'

latitude_ID = '18770'
longitude_ID = '18771'
timestamp_ID = '18772'
reading_ID = '18773'
depth_ID = '18774'
type_ID = '18775'

if(len(sys.argv)<3):
    print('You need to specify the dataset to use and what to start the datapoint counter at using command line arguments like this: python /path/to/script ID_OF_DATASET COUNTER_START')
    exit()

try:
    datapoint_counter = int(sys.argv[2])
except:
    print('invalid argument to start datapoint counter must be an integer')
    exit()

dataset_ID = sys.argv[1]

print('oof2')

def get_formatted_timestamp():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

def iSense_append_data(contribution_key,dataset_ID,data):
    payload = {
        'contribution_key':contribution_key,
        'id':dataset_ID,
	'data':data
    }
    headers = {'content-type':'application/json'}
    request = requests.post('https://isenseproject.org/api/v1/data_sets/append',data=json.dumps(payload),headers=headers)
    #print(request)
    #print(request.text)
#	request.text


print('oof3')

if len(sys.argv) > 3:
    base_station_feather_identifier = sys.argv[3]
else:
    base_station_feather_identifier = '/dev/ttyACM0'

print('Will attempt to communicate with feather at: ' + base_station_feather_identifier)




try:
    base_station_feather = serial.Serial(base_station_feather_identifier,9600)
except KeyboardInterrupt as e:
    raise
except:
    e = sys.exc_info()[0]
    print(e)
    print('unable to connect with base station feather - device not found at specified address')
    raise

while True:
    try:
        if(datapoint_counter>=dataset_limit):
            dataset_ID=init_new_dataset()
            datapoint_counter=0
        input = base_station_feather.readline()#.decode('UTF-8')
        print('The input I got was:', input)
        try:
            feather_identifier, sensor_identifier, reading = input.split(':')
            #feather_indentifer = str(feather_identifier)
            #sensor_identifier = str(sensor_identifier)
            #reading = str(reading)
        except ValueError:
            print('malformed message - wrong number of delimeters')
            raise
        try:
            print('feather identifier was: ',feather_identifier)
            print('sensor identifier was: ', sensor_identifier)
            print('reading was: ', reading)
            data = {
                timestamp_ID:[get_formatted_timestamp()],
                latitude_ID:[node_ids_to_position_information[feather_identifier]['lat']],
                longitude_ID:[node_ids_to_position_information[feather_identifier]['long']],
                depth_ID:[node_ids_to_position_information[feather_identifier]['depth']],
                reading_ID:[reading],
                type_ID:[feather_ids_to_address_dictionaries_for_descriptions[feather_identifier][sensor_identifier]]
            }
        except KeyError:
            print('unexpected sensor identifier encountered - no corresponding feild in iSense')
            raise
        try:
            iSense_append_data(contribution_key, dataset_ID, data)
            datapoint_counter=datapoint_counter+1
        except requests.exceptions.RequestException as e:
            print('error making request to iSense - no internet or issues with iSense')
            raise
    except KeyboardInterrupt as e:
        raise
    except ValueError as e:
	pass
    except:
        e = sys.exc_info()[0]
        print(e)
        raise

