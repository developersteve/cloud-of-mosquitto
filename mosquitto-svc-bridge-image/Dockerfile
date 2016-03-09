FROM debian:jessie

MAINTAINER Kyle. Bai <kyle.b@inwinstack.com>

# ENV DEBIAN_FRONTEND noninteractive

USER root

RUN apt-get update && apt-get install -y wget

RUN wget -q -O - http://repo.mosquitto.org/debian/mosquitto-repo.gpg.key | apt-key add -
RUN wget -q -O /etc/apt/sources.list.d/mosquitto-jessie.list http://repo.mosquitto.org/debian/mosquitto-jessie.list
RUN apt-get update
RUN apt-get install -y mosquitto

COPY etc/mosquitto/conf.d/ /etc/mosquitto/conf.d/

COPY config-and-run.sh /usr/sbin/
RUN chown root.root /usr/sbin/config-and-run.sh
RUN chmod 700 /usr/sbin/config-and-run.sh

EXPOSE 1883

CMD ["/usr/sbin/config-and-run.sh"]
