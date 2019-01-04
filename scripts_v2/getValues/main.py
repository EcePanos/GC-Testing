import json
from flask import jsonify
from googleapiclient import discovery
from google.oauth2 import service_account



def getValues(request):
    data=open("metal-hologram-132310-a7ebd7309566.json").read()
    info=json.loads(data)

    #Local testing command, change before deploy
    request_json=request.get_json()

    credentials = service_account.Credentials.from_service_account_info(info)
    resources=[]

    key=request_json["key"]

    service = discovery.build('compute', 'v1', credentials=credentials)
    project = 'metal-hologram-132310'
    zone = 'us-central1-c'
    request = service.instances().list(project=project, zone=zone)
    response = request.execute()
    instances = []
    for item in response["items"]:
        for item_key in item["labels"].keys():
            if(item_key==key):
                resources.append(item["labels"][item_key])

    service = discovery.build('cloudfunctions', 'v1', credentials=credentials)
    parent='projects/metal-hologram-132310/locations/-'
    request = service.projects().locations().functions().list(parent=parent)
    response = request.execute()
    #functions=response.get_json()
    for item in response["functions"]:
        for item_key in item["labels"].keys():
            if (item_key == key):
                resources.append(item["labels"][item_key])
    values=list(set(resources))

    output = {
        "statusCode": 200,
        "body": json.dumps(values)
    }

    return jsonify(output), 200



