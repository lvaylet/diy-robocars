FROM arm32v7/node:10-slim

ENV INITSYSTEM on

RUN apt-get update && apt-get install -y \
      minicom \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY package.json ./

RUN JOBS=MAX npm install --production

COPY . .

CMD [ "bash", "start.sh" ]
