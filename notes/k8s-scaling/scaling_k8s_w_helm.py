from time import sleep
import subprocess
import yaml
import argparse
from pprint import pprint

description = "Helm deployment manual scaling demo"
parser = argparse.ArgumentParser(description=description)
parser.add_argument("-n", "--namespace", help="namespace of K8s deployment")
parser.add_argument("-c", "--chart-name", help="helm chart name")
parser.add_argument("-a", "--application-name", help="K8s application name")
parser.add_argument("-r", "--replica-count", help="new replica number")
args = parser.parse_args()

kubectl_command: str = "/snap/bin/kubectl"
helm_command: str = "/snap/bin/helm"
namespace: str = args.namespace
chart_name: str = args.chart_name
application_name: str = args.application_name

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
command = f"{helm_command} get manifest {chart_name} --namespace={namespace}"

out = subprocess.check_output(command, shell=True)

output = out.decode("utf-8").strip()

manifests = yaml.load_all(output, Loader=yaml.SafeLoader)

allowed_kinds = ("deployment", "statefulset", "replicaset", "replicationcontroller")
# This way we can find the kind of the k8s object
wanted_manifest = None
for manifest in manifests:
    if (
        manifest['kind'].lower() in allowed_kinds
        and any(manifest['metadata']['name'] == name for name in name_list)
    ):
        wanted_manifest = manifest
        print(manifest)

# Now, we have the kind of k8s object
kind = wanted_manifest['kind'].lower()
name = wanted_manifest.get('metadata', {}).get('name')

# Control replica count
command = f"{kubectl_command} get {kind} {name} --namespace={namespace} -o=yaml"

out = subprocess.check_output(command, shell=True)

output = out.decode("utf-8").strip()

data = yaml.load(output, Loader=yaml.SafeLoader)

pprint(data)

try:
    replicas = data['status']['replicas']
except KeyError:
    replicas = data['spec']['replicas']

print(f"Current replica number: {replicas}")
# Time to scale
new_replica = int(args.replica_count)
print(f"New replica number: {new_replica}")

if new_replica != replicas:
    command = f"{kubectl_command} scale --namespace={namespace} {kind} {name} --replicas={new_replica} -o=yaml"

    out = subprocess.check_output(command, shell=True)

    output = out.decode("utf-8").strip()

    data = yaml.load(output, Loader=yaml.SafeLoader)

while new_replica != replicas:
    print("Waiting until all replicas are ready!")
    sleep(5)
    # Control replica count
    command = f"{kubectl_command} get {kind} {name} --namespace={namespace} -o=yaml"

    out = subprocess.check_output(command, shell=True)

    output = out.decode("utf-8").strip()

    data = yaml.load(output, Loader=yaml.SafeLoader)

    try:
        replicas = data['status']['readyReplicas']
    except KeyError:
        replicas = data['spec']['replicas']

print("Done!")
