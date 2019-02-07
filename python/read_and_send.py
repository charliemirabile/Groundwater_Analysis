import serial,requests,json,time,datetime,sys

base_station_feather_identifier = '/dev/ttyACM0'

sensor_identifiers_to_iSense_feilds = {
        #must add
    }

timestamp_feild_identifier = '' #must add

iSense_contribution_key = 'rpi-key'

iSense_dataset_id = '' #must add

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
        input = str(base_station_feather.readline())
        
        print(input)
        
        try:
            sensor_identifier,reading = input.split(':')
        except ValueError as e:
            print(e)
            print('malformed message - no delimeter or more than one')
        try:
            iSense_feild_identifier = sensor_identifiers_to_iSense_feilds[sensor_identifier]
        except KeyError as e:
            print(e)
            print('unexpected sensor identifier encountered - no corresponding feild in iSense')
        data = {
                iSense_feild_identifier:[reading],
                timestamp_feild_identifier:[get_formatted_timestamp()]
            }
        try:
            iSense_append_data(iSense_contribution_key,iSense_dataset_id,data)
        except requests.exceptions.RequestException as e:
            print(e)
            print('error making request to iSense - no internet or issues with iSense')
    except KeyboardInterrupt as e:
        raise
    except:
        e = sys.exc_info()[0]
        print(e)
        
    
    
    
    