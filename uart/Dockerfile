FROM resin/raspberrypi3-node:9

ENV INITSYSTEM=on

# Install GCC and Python libraries
RUN apt-get update && apt-get install -y \
      minicom \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install

COPY . .

CMD [ "bash", "start.sh" ]
