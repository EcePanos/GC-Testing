import json
from flask import jsonify
from googleapiclient import discovery
from google.oauth2 import service_account



def getByTag(request):
    data = open("metal-hologram-132310-a7ebd7309566.json").read()
    info = json.loads(data)
    credentials = service_account.Credentials.from_service_account_info(info)
    service = discovery.build('compute', 'v1', credentials=credentials)

    #Local testing command, change to get_json for deployment
    request_json = request.get_json()
    # Project ID for this request.
    project = 'metal-hologram-132310'
    # The name of the zone for this request.
    zone = 'us-central1-c'
    key = request_json['key']
    value = request_json['value']
    filter = 'labels.' + key + '=' + value[0]
    # labels.hat=red
    # Name of the instance resource to start.
    # instance = 'instance-1'
    request = service.instances().list(project=project, zone=zone, filter=filter)
    response = request.execute()

    resources = []
    if("items" in response):
        for item in response["items"]:
            instance = {}
            instance["id"] = item["id"]
            instance["name"] = item["name"]
            instance["provider"] = "google"
            instance["tags"] = []

            for key in item["labels"].keys():
                instance["tags"].append({"key": key, "value": item["labels"][key]})

            instance["type"] = "instance"
            resources.append(instance)

    service = discovery.build('cloudfunctions', 'v1', credentials=credentials)
    parent = 'projects/metal-hologram-132310/locations/-'
    request = service.projects().locations().functions().list(parent=parent)
    functions = request.execute()
    # functions=response.get_json()

    if("functions" in functions):
        for function in functions["functions"]:
            label={request_json["key"]:request_json["value"]}
            if (function["labels"] == label):
                for item in functions["functions"]:
                    function = {}
                    function["id"] = item["name"]
                    function["name"] = item["name"]
                    function["provider"] = "google"
                    function["tags"] = []

                    for key in item["labels"].keys():
                        function["tags"].append({"key": key, "value": item["labels"][key]})

                    function["type"] = "function"
                    resources.append(function)

    #Change to return for deployment
    output = {
        "statusCode": 200,
        "body": json.dumps(resources)
    }

    return jsonify(output), 200



