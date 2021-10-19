# Run docker container locally

`./docker.sh`

# GCloud

Build & upload to gcloud: `gcloud builds submit --tag gcr.io/typeworld2/messagequeue`

# Attach docker output to SSH shell

`docker attach $(echo $(docker container ls) | cut -d ' ' -f9)`

# Log into container:

`docker exec -it $(echo $(docker container ls) | cut -d ' ' -f9) /bin/bash`

Reload Compute Engine: `gcloud compute instances update-container messagequeue`

# Limitations:

[Number of connections:](https://stackoverflow.com/a/31303917) `ulimit -n` 

[Global limit:](https://askubuntu.com/questions/26985/what-is-a-safe-ulimit-ceiling/27268#27268) `cat /proc/sys/fs/file-max` 

ssh into docker:
`sudo docker ps -a`
`sudo docker exec -it 77a14e3cb2b4 bash`
