import requests,json,time,datetime,random

def postToAppendData(contributionKey,datasetID,data):
    payload = {
        'contribution_key':contributionKey,
        'id':datasetID,
        'data':data
    }
    headers = {'content-type':'application/json'}
    request = requests.post('https://isenseproject.org/api/v1/data_sets/append',data=json.dumps(payload),headers=headers)
    #print(request.url)
    #print(request.text)
    

def getFormattedTimestamp():
    currentTime = time.time()
    formattedTime = datetime.datetime.fromtimestamp(currentTime).strftime('%Y-%m-%d %H:%M:%S')
    return formattedTime

a=0
def createData():
    global a
    a+=1
    data = {
            '18062': [a],
            '18063': [random.randint(0,100)],
            '18064': ['Hello World!'],
            '18061': [getFormattedTimestamp()]
        } 
    return data

def createEmptyDataset():
    payload = {
        'title': 'R-Pi dataset',
        'contribution_key': 'rpi-key',
        'contributor_name': 'Raspberry Pi',
        'data':{
            'Number_1': [0],
            'Number_2': [0],
            'Text_1': ['first point'],
            'Timestamp': [getFormattedTimestamp()]
        }
    }
    headers = {'content-type':'application/json'}
    request = requests.post('https://isenseproject.org/api/v1/projects/3645/jsonDataUpload',data=json.dumps(payload),headers=headers)
    print(request.url)
    print(request.text)

#createEmptyDataset()
for i in range(0,500):
    postToAppendData('rpi-key',100235,createData())
