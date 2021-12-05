FROM ubuntu:18.04

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV RELEASE=ReleaseTEN
ENV REPOSITORY=stable
ENV REPOSITORY_BASE=https://osm-download.etsi.org/repository/osm/debian

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y curl gnupg2 software-properties-common

RUN CLIENT_RELEASE=${RELEASE#"-R "} && \
    CLIENT_REPOSITORY_KEY="OSM%20ETSI%20Release%20Key.gpg" && \
    CLIENT_REPOSITORY=${REPOSITORY#"-r "} && \
    CLIENT_REPOSITORY_BASE=${REPOSITORY_BASE#"-u "} && \
    key_location=$CLIENT_REPOSITORY_BASE/$CLIENT_RELEASE/$CLIENT_REPOSITORY_KEY && \
    curl $key_location > /tmp/key && \
    apt-key add /tmp/key && \
    DEBIAN_FRONTEND=noninteractive add-apt-repository -y "deb [arch=amd64] $CLIENT_REPOSITORY_BASE/$CLIENT_RELEASE $CLIENT_REPOSITORY osmclient IM"

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3-pip && \
    LC_ALL=C python3 -m pip install -U pip && \
    LC_ALL=C python3 -m pip install -U python-magic pyangbind verboselogs && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3-osm-im python3-osmclient

RUN bash if [ -f /usr/lib/python3/dist-packages/osm_im/requirements.txt ]; then python3 -m pip install -r /usr/lib/python3/dist-packages/osm_im/requirements.txt; fi

RUN bash if [ -f /usr/lib/python3/dist-packages/osmclient/requirements.txt ]; then apt-get install -y libcurl4-openssl-dev libssl-dev && python3 -m pip install -r /usr/lib/python3/dist-packages/osmclient/requirements.txt; fi

ARG OSM_NBI_HOST=localhost
ARG OSM_NBI_PORT=9999

ENV OSM_HOSTNAME=$OSM_NBI_HOST:$OSM_NBI_PORT

CMD [ "sleep", "infinity" ]
