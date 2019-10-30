import serial,requests,json,time,datetime,sys

config = {
    'iSense_info':
    {
        'dataset_id':'<TEMP>',
        'contribution_key':'<TEMP>',
        'feild_identifiers':
        {
            'timestamp_identifier':'<TEMP>',
            'reading_identifier':'<TEMP>',
            'node_level':
            {
                'lat':'<TEMP>',
                'long':'<TEMP>'
            },
            'sensor_level':
            {
                'type':'<TEMP>',
                'depth':'<TEMP>'
            }
        }
    },
    'nodes':
    {
        '1337':
        {
            'node_level':
            {
                'lat':'<TEMP>',
                'long':'<TEMP>'
            },
            'sensors':
            {
                '67':
                {
                    'type':'<TEMP>',
                    'depth':'<TEMP>'
                },
                '68':
                {
                    'type':'<TEMP>',
                    'depth':'<TEMP>'
                },
                '69':
                {
                    'type':'<TEMP>',
                    'depth':'<TEMP>'
                }
            }
        },
        '1338':
        {
            'node_level':
            {
                'lat':'<TEMP>',
                'long':'<TEMP>'
            },
            'sensors':
            {
                '67':
                {
                    'type':'<TEMP>',
                    'depth':'<TEMP>'
                },
                '68':
                {
                    'type':'<TEMP>',
                    'depth':'<TEMP>'
                },
                '69':
                {
                    'type':'<TEMP>',
                    'depth':'<TEMP>'
                }
            }
        }
    }
}


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


iSense_field_idenfifiers = {#MUST ADD

	'timestamp' : '17090',
	'metric' : '17093',
	'latitude' : '17094',
	'longitude' : '17095',
	'depth' : '17092',
	'reading' : '17091'
}




iSense_contribution_key = 'oof'

iSense_dataset_id = 71226

def get_formatted_timestamp():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

def iSense_append_data(contribution_key,dataset_ID,data):
    payload1 = {
        'contribution_key':contribution_key,
        'id':dataset_ID,
	'data':data
    }
    payload2 = {
       'contribution_key':'oof',
       'id':71219,
       'data':data
    }
    headers = {'content-type':'application/json'}
    request1 = requests.post('https://dev.isenseproject.org/api/v1/data_sets/append',data=json.dumps(payload1),headers=headers, verify=False)
    #request2 = requests.post('https://rsense-env.j344zpn2wr.us-east-1.elasticbeanstalk.com/api/v1/data_sets/append',data=json.dumps(payload2),headers=headers, verify=False)
    #print(request)
    print(request1.text)
#    print(request2.text)
#	request.text

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
                iSense_field_idenfifiers['timestamp']:[get_formatted_timestamp()],
                iSense_field_idenfifiers['latitude']:[node_ids_to_position_information[feather_identifier]['lat']],
                iSense_field_idenfifiers['longitude']:[node_ids_to_position_information[feather_identifier]['long']],
                iSense_field_idenfifiers['depth']:[node_ids_to_position_information[feather_identifier]['depth']],
                iSense_field_idenfifiers['reading']:[reading],
                iSense_field_idenfifiers['metric']:[feather_ids_to_address_dictionaries_for_descriptions[feather_identifier][sensor_identifier]]
            }
        except KeyError:
            print('unexpected sensor identifier encountered - no corresponding feild in iSense')
            raise
        try:
            iSense_append_data(iSense_contribution_key,iSense_dataset_id,data)
        except requests.exceptions.RequestException as e:
            print('error making request to iSense - no internet or issues with iSense')
            raise
    except KeyboardInterrupt as e:
        raise
    except:
        e = sys.exc_info()[0]
        print(e)
