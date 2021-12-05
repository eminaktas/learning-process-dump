# osm-client-container

Run the osmclient as container in the same namespace of OSM.

```bash
# Create a osmclient Pod 
$ kubectl create -f osmclient-pod.yaml
# Delete the osmclient Pod
$ kubectl delete -f osmclient-pod.yaml
# or
$ kubectl delete pod osmclient -n osm 
# Exec
$ kubectl exec -it osmclient -n osm bash
```

Docker commands

```bash
# Build image
$ docker build -t eminaktas/osmclient:latest .
# Push image
$ docker push eminaktas/osmclient:latest
# Run Docker container
$ docker run -it eminaktas/osmclient:latest bash
```

After getting in container, make sure that `OSM_HOSTNAME` envrionment varible is correctly set.

## Sample commands

Add dummy vim

```bash
osm vim-create --name osm-vim --account_type dummy --auth_url http://dummy --user osm --password osm --tenant osm --description "dummy" --config '{management_network_name: mgmt}'
```

Add a K8s cluster

```bash
osm k8scluster-add --creds <config-file-path> --vim osm-vim --k8s-nets '{"net1": null}' --version '1.20' --description "OSM Internal Cluster" local-osm-k8s
```

If you installed the k8s cluster with `microk8s`, you can get the config with below command

```bash
microk8s config > /tmp/config
```

Upload a knf package

```bash
git clone https://osm.etsi.org/gitlab/vnf-onboarding/osm-packages.git
cd osm-packages
osm vnfd-create openldap_knf
osm nsd-create openldap_ns
```

Port forwarding to reach the Kubernetes services.

```bash
# NG-UI
kubectl port-forward service/ng-ui 8080:80 -n osm
# NBI
kubectl port-forward service/nbi 9999:9999 -n osm
```
