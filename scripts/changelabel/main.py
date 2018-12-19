import json
from googleapiclient import discovery
from google.oauth2 import service_account

#Carefull, the bucket referenced must contain the intended version of the file
#Must be updated to get function object before updating

def changelabel(request):
    data=open("metal-hologram-132310-a7ebd7309566.json").read()
    info=json.loads(data)
    credentials = service_account.Credentials.from_service_account_info(info)
    service = discovery.build('cloudfunctions', 'v1', credentials=credentials)

    #Actual command
    request_json=request.get_json()

    #Local testing command
    #request_json=request

    name=request_json["name"]
    get_request=service.projects().locations().functions().get(name=name)
    body=get_request.execute()
    body["labels"]=request_json["labels"]
    request = service.projects().locations().functions().patch(name=name,body=body)
    response = request.execute()
    #print(json.dumps(response))
    return json.dumps(response)

"""Local testing
test={
"name":"projects/metal-hologram-132310/locations/us-central1/functions/startvm",
"labels": {
  "funny": "joke"
}
}
#test_request=json.dumps(test)
changelabel(test)
"""
