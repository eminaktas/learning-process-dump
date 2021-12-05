FROM ubuntu:18.04

RUN apt-get update -qq && \
	apt-get install -y software-properties-common && \
	apt-add-repository -u -y ppa:juju/stable

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -y install juju

ENV JUJU_DATA=/root/.local/share/juju

CMD [ "sleep", "infinity" ]
