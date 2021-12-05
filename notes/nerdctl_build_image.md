# Build image with nerdctl

## Install

```bash
export BUILDKIT_VERSION="v0.8.1"
export ARCH=$(dpkg --print-architecture | sed 's/ppc64el/ppc64le/' | sed 's/armhf/arm-v7/')
echo "Installing buildkit ..."
export BUILDKIT_BASE_URL="https://github.com/moby/buildkit/releases/download/${BUILDKIT_VERSION}"
curl -sSL --retry 5 --output /tmp/buildkit.tgz "${BUILDKIT_BASE_URL}/buildkit-${BUILDKIT_VERSION}.linux-${ARCH}.tar.gz"
tar -C /usr/local -xzvf /tmp/buildkit.tgz
rm -rf /tmp/buildkit.tgz
chmod 755 /usr/local/bin/buildctl
chmod 755 /usr/local/bin/buildkit-runc
chmod 755 /usr/local/bin/buildkitd
```

## Run buildkitd

```bash
buildkitd
```

## Build image

```bash
export DOCKER_TAG=dev
sudo nerdctl --namespace k8s.io --address /var/snap/microk8s/common/run/containerd.sock build --no-cache -t opensourcemano/lcm:${DOCKER_TAG} --build-arg PYTHON3_OSM_COMMON_URL=localhost:8080/common.deb --build-arg PYTHON3_N2VC_URL=localhost:8080/n2vc.deb --build-arg PYTHON3_OSM_LCM_URL=localhost:8080/lcm.deb devops/docker/LCM/.
```
