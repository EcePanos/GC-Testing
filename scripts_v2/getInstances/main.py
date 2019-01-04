import json
from flask import jsonify
from googleapiclient import discovery
from google.oauth2 import service_account

def getInstances(request):
    data=open("metal-hologram-132310-a7ebd7309566.json").read()
    info=json.loads(data)
    credentials = service_account.Credentials.from_service_account_info(info)
    service = discovery.build('compute', 'v1', credentials=credentials)
    #request_json=request.get_json()
    # Project ID for this request.
    project = 'metal-hologram-132310'
    # The name of the zone for this request.
    zone = 'us-central1-c'

    request = service.instances().list(project=project, zone=zone)
    response = request.execute()
    instances=[]
    for item in response["items"]:
        instance={}
        instance["id"]=item["id"]
        instance["name"]=item["name"]
        instance["provider"]="google"
        instance["tags"]=[]

        for key in item["labels"].keys():
            instance["tags"].append({"key": key, "value": item["labels"][key]})

        instance["type"]="instance"
        instances.append(instance)
    #Local testing
    #print(json.dumps(instances))

    output = {
        "statusCode": 200,
        "body": json.dumps(instances)
    }

    return jsonify(output), 200

