import json
from flask import jsonify
from googleapiclient import discovery
from google.oauth2 import service_account



def getKeys(request):
    data=open("metal-hologram-132310-a7ebd7309566.json").read()
    info=json.loads(data)

    credentials = service_account.Credentials.from_service_account_info(info)
    resources=[]

    service = discovery.build('compute', 'v1', credentials=credentials)
    project = 'metal-hologram-132310'
    zone = 'us-central1-c'
    request = service.instances().list(project=project, zone=zone)
    response = request.execute()
    instances = []
    for item in response["items"]:
        for key in item["labels"].keys():
            resources.append(key)

    service = discovery.build('cloudfunctions', 'v1', credentials=credentials)
    parent='projects/metal-hologram-132310/locations/-'
    request = service.projects().locations().functions().list(parent=parent)
    response = request.execute()
    #functions=response.get_json()
    for item in response["functions"]:
        for key in item["labels"].keys():
            resources.append(key)
    keys=list(set(resources))


    # Local testing
    #print(json.dumps(resources))

    output = {
        "statusCode": 200,
        "body": json.dumps(keys)
    }

    return jsonify(output), 200


