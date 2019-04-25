import requests,json,time,datetime,random

def postToAppendData(contributionKey,datasetID,data):
    payload = {
        'contribution_key':contributionKey,
        'id':datasetID,
        'data':data
    }
    headers = {'content-type':'application/json'}
    request = requests.post('https://isenseproject.org/api/v1/data_sets/append',data=json.dumps(payload),headers=headers)
    print(request)
    print(request.url)
    print(request.text)

def getFormattedTimestamp():
    currentTime = time.time()
    formattedTime = datetime.datetime.fromtimestamp(currentTime).strftime('%Y-%m-%d %H:%M:%S')
    return formattedTime

a=0
def createData():
    global a
    a+=1
    data = {
            '18368': [a],
            '18369': [str(random.randint(0,100))],
            '18370': ['Hello World!'],
            '18367': [getFormattedTimestamp()]
        } 
    return data

def createEmptyDataset():
    payload = {
        'title': 'R-Pi dataset',
        'contribution_key': 'keykey',
        'contributor_name': 'Raspberry Pi',
        'data':{
            '18367': [getFormattedTimestamp()],
            '18370': ['asdfasdf'],
            '18365': ['37'],
            '18366': ['37'],
            '18368': ['5'],
            '18369': [5]
        }
    }
    headers = {'content-type':'application/json'}
    request = requests.post('https://isenseproject.org/api/v1/projects/3651/jsonDataUpload',data=json.dumps(payload),headers=headers)
    print(request)
    print(request.url)
    print(request.text)

#createEmptyDataset()
#for i in range(0,500):
#postToAppendData('keykey',101110,createData())
createEmptyDataset()
