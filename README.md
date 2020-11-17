# Run docker container locally

`./docker.sh`

# GCloud

Build & upload to gcloud: `gcloud builds submit --tag gcr.io/typeworld2/messagequeue`

Reload Compute Engine: `gcloud compute instances update-container messagequeue`

# Limitations:

[Number of connections:](https://stackoverflow.com/a/31303917) `ulimit -n` 

[Number of connections:](https://stackoverflow.com/a/31303917) `ulimit -n` 
