# https://hub.docker.com/repository/docker/typeworld/pyzmq-draft
FROM typeworld/pyzmq-draft:1.0

COPY . /app
WORKDIR /app
CMD ["/app/startup.sh"]
