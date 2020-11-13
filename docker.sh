# Kill & Delete
docker kill messagequeue
docker container rm messagequeue
docker rmi messagequeue:1.0

set -e

# Build
docker build --tag messagequeue:1.0 .

# Run
docker run -p 8080:8080 -p 5556:5556/udp -p 5556:5556 -d --name messagequeue messagequeue:1.0
