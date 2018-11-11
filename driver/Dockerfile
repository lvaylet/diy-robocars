FROM resin/raspberrypi3-python:3.6-slim

LABEL maintainer="Laurent Vaylet <laurent.vaylet@gmail.com>"

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

COPY . ./

CMD [ "bash", "start.sh" ]
