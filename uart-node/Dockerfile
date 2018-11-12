FROM resin/raspberrypi3-node:9

LABEL maintainer="Laurent Vaylet <laurent.vaylet@gmail.com>"

ENV INITSYSTEM=on

RUN apt-get update && apt-get install -y \
      minicom \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY package.json package-lock.json ./
RUN JOBS=MAX npm install --production

COPY . ./

CMD [ "bash", "start.sh" ]
