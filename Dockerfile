# https://hub.docker.com/repository/docker/typeworld/pyzmq-draft
FROM typeworld/pyzmq:1.0

EXPOSE 80
EXPOSE 5556
EXPOSE 5556/udp

RUN pip install flask gunicorn
RUN apt-get update && apt-get install -y gcc python3-dev iproute2 && pip install psutil

COPY . /app
WORKDIR /app
CMD ["/app/startup.sh"]
