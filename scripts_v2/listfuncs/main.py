import json
from googleapiclient import discovery
from google.oauth2 import service_account



def listfuncs(request):
    data=open("metal-hologram-132310-a7ebd7309566.json").read()
    info=json.loads(data)

    #request_json=request.get_json()

    #local testing command
    request_json=request

    credentials = service_account.Credentials.from_service_account_info(info)
    service = discovery.build('cloudfunctions', 'v1', credentials=credentials)
    parent='projects/metal-hologram-132310/locations/-'
    request = service.projects().locations().functions().list(parent=parent)
    functions = request.execute()
    #functions=response.get_json()
    results=[]
    for function in functions["functions"]:
        if(function["labels"]==request_json["labels"]):
            results.append(function)
    #return(json.dumps(results))
    print(json.dumps(results))


test={
  "labels":{
    "a":"dino"
  }
}
#test_request=json.dumps(test)
listfuncs(test)

