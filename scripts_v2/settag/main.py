import json
from googleapiclient import discovery
from google.oauth2 import service_account

#Need the name and label fingerprint for the existing label. Completely
#replaces previous label. Must be updated to get the label fingerprint

def settag(request):
    data=open("metal-hologram-132310-a7ebd7309566.json").read()
    info=json.loads(data)
    credentials = service_account.Credentials.from_service_account_info(info)
    service = discovery.build('compute', 'v1', credentials=credentials)
    request_json=request.get_json()

    #Use command bellow for local testing
    #request_json=request

    # Project ID for this request.
    project = 'metal-hologram-132310'
    # The name of the zone for this request.
    zone = 'us-central1-c'
    # Name of the instance resource to start.
    instance = request_json['instance']
    print(instance)
    key=request_json['tag']['key']
    print(key)
    value=request_json['tag']['value']
    print(value)
    get_request=service.instances().get(project=project,zone=zone,instance=instance)
    get_response=get_request.execute()
    labelfingerprint=get_response["labelFingerprint"]
    print(labelfingerprint)
    instances_set_labels_request_body = {
        "labels": {
            key: value,
            },
        "labelFingerprint": labelfingerprint
        }
    request = service.instances().setLabels(project=project, zone=zone, instance=instance, body=instances_set_labels_request_body)
    response = request.execute()

"""Local testing request

test={
  "instance":"instance-1",
  "tag":{
    "key":"blue",
    "value":"chair"
  }
}
#test_request=json.dumps(test)
settag(test)

"""
