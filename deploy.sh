LABEL=$(date "+%Y%m%dt%H%M%S")
GOOGLE_COMPUTE_ZONE="us-east1-b"
GOOGLE_COMPUTE_MACHINETYPE="e2-micro"
MACHINENAME="messagequeue"
IP_ADDRESS=$(gcloud compute addresses list --filter="name=$MACHINENAME" | awk 'NR==2 {print $2}')
NEW_INSTANCE="$MACHINENAME-$LABEL"
OLD_INSTANCE=$(gcloud compute instances list --filter="EXTERNAL_IP=('$IP_ADDRESS')" | awk 'NR==2 {print $1}')

echo "Building $MACHINENAME:$LABEL"
echo "GOOGLE_COMPUTE_ZONE: $GOOGLE_COMPUTE_ZONE"
echo "GOOGLE_COMPUTE_MACHINETYPE: $GOOGLE_COMPUTE_MACHINETYPE"
echo "OLD_INSTANCE: $OLD_INSTANCE"
echo "NEW_INSTANCE: $NEW_INSTANCE"
echo "IP: $IP_ADDRESS"

# Copy APIKEY
echo "Reading APIKEY" 
DOCKER_ID=$(gcloud compute ssh --zone $GOOGLE_COMPUTE_ZONE $OLD_INSTANCE -- 'docker ps' | awk '$2 ~ /messagequeue/ {print $1}')
echo "DOCKER_ID: $DOCKER_ID"
APIKEY=$(gcloud compute ssh --zone $GOOGLE_COMPUTE_ZONE $OLD_INSTANCE -- "docker exec $DOCKER_ID env" | awk -F '=' '{if($1=="APIKEY") print $2}')
echo "APIKEY: $APIKEY"

set -e
if [$APIKEY == ""]; then
    echo "Error: APIKEY is empty"
    exit 1
fi

# Build
echo "Building new image gcr.io/typeworld2/$MACHINENAME:$LABEL" 
gcloud builds submit --tag gcr.io/typeworld2/$MACHINENAME:$LABEL

# Run new instance
echo "Creating new instance: $NEW_INSTANCE"
gcloud beta compute instances create-with-container ${NEW_INSTANCE} \
    --machine-type=${GOOGLE_COMPUTE_MACHINETYPE}\
    --container-image=gcr.io/typeworld2/${MACHINENAME}:${LABEL} \
    --container-env="APIKEY=$APIKEY" \
    --tags http-server,https-server \
    --zone ${GOOGLE_COMPUTE_ZONE}

# # Get Instance ID
# echo "Getting Instance ID"
# NEW_INSTANCE_ID=$(gcloud compute instances describe --zone $GOOGLE_COMPUTE_ZONE $NEW_INSTANCE --format="flattened(id)" | awk '{print $2}')
# echo "Setting Instance ID"
# NEW_DOCKER_ID=$(gcloud compute ssh --zone $GOOGLE_COMPUTE_ZONE $NEW_INSTANCE -- 'docker ps' | awk 'NR==2 {print $1}')
# gcloud compute ssh --zone $GOOGLE_COMPUTE_ZONE $NEW_INSTANCE -- "docker exec $NEW_DOCKER_ID export INSTANCE_ID=$NEW_INSTANCE_ID"

# Remove ephemeral IP address from new instance
echo "Removing ephemeral IP address from instance: $NEW_INSTANCE"
gcloud compute instances delete-access-config ${NEW_INSTANCE} \
    --access-config-name "external-nat" \
    --zone ${GOOGLE_COMPUTE_ZONE}

# Remove reserved IP address from old instance
# Ignore error if there is no access config present
if [ "$OLD_INSTANCE" != "null" ]; then
    echo "Removing reserved IP address from instance: $OLD_INSTANCE"
    gcloud compute instances delete-access-config ${OLD_INSTANCE} \
        --access-config-name "External NAT" \
        --zone ${GOOGLE_COMPUTE_ZONE} || true
fi

# Assign reserved IP address to new instance
echo "Assign reserved IP address to new instance: $NEW_INSTANCE"
gcloud compute instances add-access-config ${NEW_INSTANCE} \
    --access-config-name "External NAT" --address ${IP_ADDRESS} \
    --zone ${GOOGLE_COMPUTE_ZONE}

# Shutdown old instance
if [ "$OLD_INSTANCE" != "null" ]; then
    echo "Shutdown old instance: $OLD_INSTANCE"
    gcloud compute instances stop ${OLD_INSTANCE} --zone ${GOOGLE_COMPUTE_ZONE}
    gcloud compute instances delete ${OLD_INSTANCE} --quiet --zone=${GOOGLE_COMPUTE_ZONE}
fi
