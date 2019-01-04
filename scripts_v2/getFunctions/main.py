import json
from flask import jsonify
from googleapiclient import discovery
from google.oauth2 import service_account



def getFunctions(request):
    data=open("metal-hologram-132310-a7ebd7309566.json").read()
    info=json.loads(data)

    credentials = service_account.Credentials.from_service_account_info(info)
    service = discovery.build('cloudfunctions', 'v1', credentials=credentials)
    parent='projects/metal-hologram-132310/locations/-'
    request = service.projects().locations().functions().list(parent=parent)
    response = request.execute()
    #functions=response.get_json()
    functions = []

    for item in response["functions"]:

        function = {}
        function["id"] = item["name"]
        function["name"] = item["name"]
        function["provider"] = "google"
        function["tags"] = []

        for key in item["labels"].keys():
            function["tags"].append({"key": key, "value": item["labels"][key]})

        function["type"] = "function"
        functions.append(function)

    # Local testing
    #print(json.dumps(functions))
    output={
        "statusCode": 200,
        "body": json.dumps(functions)
    }

    return jsonify(output),200



