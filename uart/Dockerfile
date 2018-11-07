FROM resin/raspberrypi3-node:9

ENV INITSYSTEM=on

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install

COPY . .

CMD bash start.sh
