# Manual scaling Kubernetes objects deployed with Helm

In the previous feature, OSM is now able to scale the juju bundles via OSM now.
We should be able to scale the Pods that are deployed with Helm. In order to do the scaling we need some specific informations.
1 - K8s object kind
2 - K8s object name
3 - K8s object namespace

## How to scale a K8s object

With kubectl,

```bash
  # Scale a replicaset named 'foo' to 3.
  kubectl scale --replicas=3 rs/foo
  
  # Scale a resource identified by type and name specified in "foo.yaml" to 3.
  kubectl scale --replicas=3 -f foo.yaml
  
  # If the deployment named mysql's current size is 2, scale mysql to 3.
  kubectl scale --current-replicas=2 --replicas=3 deployment/mysql
  
  # Scale multiple replication controllers.
  kubectl scale --replicas=5 rc/foo rc/bar rc/baz
  
  # Scale statefulset named 'web' to 3.
  kubectl scale --replicas=3 statefulset/web
```

With Python client,

```python
from kuberentes import client, config
def scale():
    config.load_kube_config()
    app_v1 = cleint.AppsV1Api()
    body = {'spec': {'replicas': 5}}
    # We have to call the specific function for the object
    result = app_v1.patch_namespaced_deployment_scale("name", "namespace", body)
    print("New replica count: {}, Old replica count: {}".format(
      result.spec.replicas, result.status.replicas
    ))
if __name__ == '__main__':
    scale()
```

Scaling deployment with Python client comes with challanges.
1 - You need to know the Api version
2 - You need to use specific function to scale the object

## How to scale K8s objects in OSM

With OSM, we need to know two things about instance that are its name and its kind.
To find out the kind, the only way to look up for the ReplicaSet, if it doesn't have ReplicaSet it's probably ReplicationController or StatefulSet.
The key part is to name of the instance with the helm deployment. In OSM, K8s Workloads could take the name of the kdu instance if below statement is avaible in the Helm charts or it will have the custom name defined here in the workload.

```yaml
  labels:
  name: {{ template "prometheus.nodeExporter.fullname" . }}
```

Even if it has static name, the OSM user should provide the name of the deployment.

## Why not upgrading Helm

Helm doesn't naturally support scaling K8s objects. We can only use `helm upgrade` to scale applications. Each upgrading helm process will create another release. We might upgrade the application thounds times. Also, it's longer process we just want to scale the workload.
