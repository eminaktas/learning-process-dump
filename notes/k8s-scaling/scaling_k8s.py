from time import sleep
import subprocess
import yaml

from pprint import pprint

kubectl_command: str = "/snap/bin/kubectl"
namespace: str = "hede"
chart_name: str = "nginx-deployment"
application_name: str = "nginx"
if application_name not in chart_name:
    name = chart_name + '-' + application_name
else:
    name = chart_name
chart_app_name = chart_name + '-' + application_name

"""
So far we have four option name can be occur in the helm deployment
1 - Chart name
2 - Chart name + application name if not chart name includes application name
3 - Charm name + application name even if chart name includes application name
4 - Application name given  by osm user
"""
name_list = [name, chart_name, application_name, chart_app_name]
print(name_list)

# Get the all replicaset defined in the namespace
command = f"{kubectl_command} --namespace={namespace} get replicaset -o=yaml"

out = subprocess.check_output(command, shell=True)

output = out.decode("utf-8").strip()

data = yaml.load(output, Loader=yaml.SafeLoader)

# This way we can find the kind of the k8s object
ownerObject = None
rs_items = data.get("items", [])
if rs_items and rs_items != []:
    for i in data['items']:
        rs_name = i['metadata']['name']
        if any(x in rs_name for x in name_list):
            for j in i['metadata'].get('ownerReferences', []):
                or_name = j['name']
                if any(x == or_name for x in name_list):
                    ownerObject = j
                    break
            else:
                print(
                    f"There is no ownerReferences in the ReplicaSet matches with namespace={namespace} and name={name}")
                if any(x == or_name for x in name_list):
                    ownerObject = i
                    break

if ownerObject is None:
    print(f"There is no avaible ReplicaSet in the namespace={namespace} and name={name}")
    print("Looking for StatefulSet if exists")
    # Get the all replicaset defined in the namespace
    command = f"{kubectl_command} --namespace={namespace} get statefulset -o=yaml"

    out = subprocess.check_output(command, shell=True)

    output = out.decode("utf-8").strip()

    data = yaml.load(output, Loader=yaml.SafeLoader)

    ss_items = data.get("items", [])
    if ss_items and ss_items != []:
        for i in data['items']:
            ss_name = i['metadata']['name']
            if any(x == ss_name for x in name_list):
                ownerObject = i

if ownerObject is None:
    print(f"There is no avaible StatefulSet in the namespace={namespace} and name={name}")
    print("Looking for ReplicationController if exists")
    # Get the all replicaset defined in the namespace
    command = f"{kubectl_command} --namespace={namespace} get replicationcontroller -o=yaml"

    out = subprocess.check_output(command, shell=True)

    output = out.decode("utf-8").strip()

    data = yaml.load(output, Loader=yaml.SafeLoader)

    rc_items = data.get("items", [])
    if rc_items and rc_items != []:
        for i in data['items']:
            rc_name = i['metadata']['name']
            if any(x == rc_name for x in name_list):
                ownerObject = i

pprint(ownerObject)

# Now, we have the kind of k8s object
owner_kind = ownerObject['kind'].lower()
owner_name = ownerObject.get('metadata', {}).get('name') or ownerObject.get('name')

# Control replica count
command = f"{kubectl_command} get {owner_kind} {owner_name} --namespace={namespace} -o=yaml"

out = subprocess.check_output(command, shell=True)

output = out.decode("utf-8").strip()

data = yaml.load(output, Loader=yaml.SafeLoader)

pprint(data)

try:
    replicas = data['status']['replicas']
except KeyError:
    replicas = data['spec']['replicas']

print(f"Replica number: {replicas}")
# Time to scale
new_replica = 10
command = f"{kubectl_command} scale --namespace={namespace} {owner_kind} {owner_name} --replicas={new_replica} -o=yaml"

out = subprocess.check_output(command, shell=True)

output = out.decode("utf-8").strip()

data = yaml.load(output, Loader=yaml.SafeLoader)

pprint(data)

while new_replica != replicas:
    print("Waiting until all replicas are ready!")
    sleep(5)
    # Control replica count
    command = f"{kubectl_command} get {owner_kind} {owner_name} --namespace={namespace} -o=yaml"

    out = subprocess.check_output(command, shell=True)

    output = out.decode("utf-8").strip()

    data = yaml.load(output, Loader=yaml.SafeLoader)

    try:
        replicas = data['status']['readyReplicas']
    except KeyError:
        replicas = data['spec']['replicas']

print("Done!")
