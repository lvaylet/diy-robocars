FROM arm32v7/nginx:1.15

# The services to serve are loaded dynamically from config files on startup.
# Clone an existing pair of config files in './etc/conf.d/' to serve an extra
# service defined in 'docker-compose.yml'.
COPY ./etc/ /etc/nginx/
