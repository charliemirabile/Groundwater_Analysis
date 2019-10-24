import serial,requests,json,time,datetime,sys

dataset_base_name = 'BoatHouseTest'
contribution_key = 'python'
contributor_name = 'Raspberry Pi'
project_ID = '3744'
dataset_ID = '103753'

latitude_ID = '18770'
longitude_ID = '18771'
timestamp_ID = '18772'
reading_ID = '18773'
depth_ID = '18774'
type_ID = '18775'


def append(data):
    payload = {
        'contribution_key':contribution_key,
        'id':dataset_ID,
        'data':data
    }
    headers = {'content-type':'application/json'}
    request = requests.post('https://isenseproject.org/api/v1/data_sets/append',data=json.dumps(payload),headers=headers)
    print(request)
    print(request.url)
    print(request.text)

def current_timestamp():
    currentTime = time.time()
    formattedTime = datetime.datetime.fromtimestamp(currentTime).strftime('%Y-%m-%d %H:%M:%S')
    return formattedTime


def init_new_dataset():
    payload = {
        'title': dataset_base_name+datetime.datetime.fromtimestamp(time.time()).strftime('_%Y_%m_%d'),
        'contribution_key': contribution_key,
        'contributor_name': contributor_name,
        'data':{
            latitude_ID:['0'],
            longitude_ID:['0'],
            timestamp_ID:[current_timestamp()],
            reading_ID:['-1'],
            depth_ID:['-1'],
            type_ID:['NULL']
        }
    }
    headers = {'content-type':'application/json'}
    request = requests.post('https://isenseproject.org/api/v1/projects/'+project_ID+'/jsonDataUpload',data=json.dumps(payload),headers=headers)
    #print(request)
    #print(request.url)
    print(request.text)
    return request.json()['id']



feather_ids_to_address_dictionaries_for_descriptions = {
	'1337':
	{
		'7':'battery',
		'20':'temperature',
		'21':'conductivity',
                '30':'temperature',
                '31':'conductivity'
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



iSense_contribution_key = 'test'

iSense_dataset_id = 101609

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






DATA_LIMIT = 500
counter = 0



if len(sys.argv) > 1:
    base_station_feather_identifier = sys.argv[1]
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
        if(counter>=DATA_LIMIT):
            iSense_dataset_id=init_new_dataset()
            counter=0
        input = base_station_feather.readline().decode('UTF-8')
        print(input)
        try:
            feather_identifier, sensor_identifier, reading = input.split(':')
            #feather_indentifer = str(feather_identifier)
            #sensor_identifier = str(sensor_identifier)
            #reading = str(reading)
        except ValueError:
            print('malformed message - wrong number of delimeters')
            raise
        try:
            print(feather_identifier)
            print(sensor_identifier)
            print(reading)
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
            iSense_append_data(iSense_contribution_key,iSense_dataset_id,data)
            counter=counter+1
        except requests.exceptions.RequestException as e:
            print('error making request to iSense - no internet or issues with iSense')
            raise
    except KeyboardInterrupt as e:
        raise
    except:
        e = sys.exc_info()[0]
        print(e)

