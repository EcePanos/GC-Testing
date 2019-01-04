import json
from googleapiclient import discovery
from google.oauth2 import service_account

def deletevm(request):
    data=open("metal-hologram-132310-a7ebd7309566.json").read()
    info=json.loads(data)
    credentials = service_account.Credentials.from_service_account_info(info)
    request_json = request.get_json()
    service = discovery.build('compute', 'v1', credentials=credentials)

    # Project ID for this request.
    project = 'metal-hologram-132310'

    # The name of the zone for this request.
    zone = 'us-central1-c'

    # Name of the instance resource to start.
    instance = request["name"]

    request = service.instances().delete(project=project, zone=zone, instance=instance)
    response = request.execute()
    return json.dumps(response)
