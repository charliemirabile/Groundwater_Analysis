import serial,requests,json,time,datetime,sys,sqlite3

#Constants
DATASET_BASE_NAME = 'Production'
CONTRIBUTION_KEY = 'python'
CONTRIBUTOR_NAME = 'Raspberry Pi'
DATASET_LIMIT = 720
PROJECT_ID = '3856'

TIMESTAMP_ID = '19412'
READING_ID = '19413'
NODE_ID = '19414'
ADDRESS_ID = '19415'

print('oof1')

#Function helpers
def get_formatted_timestamp():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

def init_new_dataset(base_station_feather):
    payload = {
        'title': DATASET_BASE_NAME+datetime.datetime.fromtimestamp(time.time()).strftime('_%Y_%m_%d_%H_%M_%S'),
        'contribution_key': CONTRIBUTION_KEY,
        'contributor_name': CONTRIBUTOR_NAME,
        'data': take_reading(base_station_feather)
    }
    headers = {'content-type':'application/json'}
    url = 'https://isenseproject.org/api/v1/projects/'+PROJECT_ID+'/jsonDataUpload'
    print(url)
    request = requests.post(url,data=json.dumps(payload),headers=headers)
    request_json=json.loads(request.text)
    print(request)
    newid = request_json['id']
    print('Switching to dataset with id: ',newid)
    return newid

def iSense_append_data(contribution_key,dataset_ID,data):
    payload = {
        'contribution_key':contribution_key,
        'id':dataset_ID,
        'data':data
    }
    headers = {'content-type':'application/json'}
    request = requests.post('https://isenseproject.org/api/v1/data_sets/append',data=json.dumps(payload),headers=headers)

def take_reading(base_station_feather):
    input = base_station_feather.readline().decode('UTF-8')
    try:
        node, address, reading = input.split(':')
        node = node.strip()
        address = address.strip()
        reading = reading.strip()
        data = {
        TIMESTAMP_ID:[get_formatted_timestamp()],
        NODE_ID:[node],
        ADDRESS_ID:[address],
        READING_ID:[reading]
        }

        print('time was: ', data[TIMESTAMP_ID])
        print('node was: ', node)
        print('address was: ', address)
        print('reading was: ', reading)

    except ValueError:
            print('malformed message - wrong number of delimeters')
            #raise
    except KeyError:
            print('unexpected sensor identifier encountered - no corresponding field in iSense')
            #raise
    push_to_db(data)
    return data

# posts data to the local database
def push_to_db(data):
    # connects to db and creates a "cursor" for navigating the database
    con = sqlite3.connect('/home/pi/Desktop/field_data.db')
    cur = con.cursor()
    
    # adds current reading to db
    cur.execute("INSERT INTO fieldDataTable VALUES (?, ?, ?, ?)", [ str(*data[TIMESTAMP_ID]) , int(*data[NODE_ID]) , int(*data[ADDRESS_ID]) , float(*data[READING_ID])])
    
    # print most recent 10 results
    cur.execute("SELECT rowid, * FROM fieldDataTable ORDER BY ROWID DESC LIMIT 10")

    fetched = cur.fetchall()

    print("ID\tTime " + "\t\t\tNode" + "\tAddress" + "\tReading")
    print("--------------------------------------------------------")
    for item in fetched:
            print(str(item[0]) + "\t" + str(item[1]) + "\t" + str(item[2]) + "\t" + str(item[3]) + "\t" + str(item[4]))
    
    print()

    # commits(saves and finalizes) the changes made to the database, and close conneciton to database 
    con.commit()
    con.close()

print('oof2')

# Connect to feather with Serial
#if len(sys.argv) > 3:
#    base_station_feather_identifier = sys.argv[3]
#else:

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

datapoint_counter = 0
dataset_ID = init_new_dataset(base_station_feather)
datapoint_counter += 1

while True:
    try:
        if(datapoint_counter>=DATASET_LIMIT):
            datapoint_counter = 0
            dataset_ID = init_new_dataset(base_station_feather)
        else:
            try:
                iSense_append_data(CONTRIBUTION_KEY, dataset_ID, take_reading(base_station_feather))
            except requests.exceptions.RequestException as e:
                print('error making request to iSense - no internet or issues with iSense')
                #raise
        datapoint_counter += 1
    except KeyboardInterrupt as e:
        raise
    except ValueError as e:
        pass
    except:
        e = sys.exc_info()[0]
        print(e)
        raise


