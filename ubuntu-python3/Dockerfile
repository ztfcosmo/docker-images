
FROM ubuntu:17.10
MAINTAINER jvansanten

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && apt-get install -y python3-astropy ipython3 \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && ln -s /usr/bin/ipython3 python \
  && pip3 install --upgrade pip