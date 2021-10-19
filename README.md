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

After an actual measurement, the number of connections maxxed out at 65K, using 1912MB memory, or 294MB per 1K connections. Therefore, a machine with roughly 3GB memory should be used (ca. 600MB system base usage + 1912MB = 2512MB)

[Number of connections:](https://stackoverflow.com/a/31303917) `ulimit -n` 

[Global limit:](https://askubuntu.com/questions/26985/what-is-a-safe-ulimit-ceiling/27268#27268) `cat /proc/sys/fs/file-max` 
