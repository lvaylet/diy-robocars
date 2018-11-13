FROM arm32v7/node:10-slim as builder
WORKDIR /app
COPY package.json ./
RUN npm install
COPY . ./
RUN npm run build

# ---

FROM arm32v7/nginx:1.15
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD [ "nginx", "-g", "daemon off;" ]
