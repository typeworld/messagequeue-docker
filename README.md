# Run docker container locally

`./docker.sh`

# GCloud

Build & upload to gcloud: `gcloud builds submit --tag gcr.io/typeworld2/messagequeue`

Set default region (if necessary): `gcloud config set run/region us-east1`

Run: `gcloud run deploy --image gcr.io/typeworld2/messagequeue --platform managed`
