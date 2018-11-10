FROM resin/raspberrypi3-python:3.6-slim

LABEL maintainer="Laurent Vaylet <laurent.vaylet@gmail.com>"

ENV INITSYSTEM=on

RUN apt-get update && apt-get install -y \
      minicom \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

COPY . ./

CMD [ "bash", "start.sh" ]
