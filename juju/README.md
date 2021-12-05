# Juju

Run juju client in Container

```bash
docker build -t eminaktas/juju-client:latest .
docker run --rm -it --name juju-client -v ~/.local/share/juju:/root/.local/share/juju eminaktas/juju-client:latest bash
```
