# Kill & Delete
docker kill messagequeue
docker container rm messagequeue
docker rmi messagequeue:1.0

set -e

# Build
docker build --tag messagequeue:1.0 .

# Run
docker run -p 80:80 -p 5556:5556/udp -p 5556:5556 -d -e APIKEY='___APIKEY___' --name messagequeue messagequeue:1.0 
