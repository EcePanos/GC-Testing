import json
from googleapiclient import discovery
from google.oauth2 import service_account



def deletefunction(request):
    data=open("metal-hologram-132310-a7ebd7309566.json").read()
    info=json.loads(data)
    credentials = service_account.Credentials.from_service_account_info(info)
    service = discovery.build('cloudfunctions', 'v1', credentials=credentials)

    #Actual command
    request_json=request.get_json()

    #Local testing command
    #request_json=request

    name=request_json["name"]
    request=service.projects().locations().functions().delete(name=name)

    response = request.execute()
    #print(json.dumps(response))
    return json.dumps(response)


