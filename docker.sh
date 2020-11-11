# Kill & Delete
docker kill messagequeue
docker container rm messagequeue
docker rmi messagequeue:1.0

set -e

# Build
docker build --tag messagequeue:1.0 .

# Run
docker run -p 5556:5556 -p 5556:5556/udp -d --name messagequeue messagequeue:1.0
