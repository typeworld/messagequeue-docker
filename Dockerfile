# https://hub.docker.com/repository/docker/typeworld/pyzmq-draft
FROM typeworld/pyzmq-draft:1.0

EXPOSE 5556/udp
EXPOSE 5556
EXPOSE 8080

RUN pip install flask gunicorn

COPY . /app
WORKDIR /app
CMD ["/app/startup.sh"]
