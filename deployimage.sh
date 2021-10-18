LABEL=$(date "+%Y%m%dt%H%M%S")
MACHINENAME="messagequeue"

echo "Building $MACHINENAME:$LABEL"

# Build
echo "Building new image gcr.io/typeworld2/$MACHINENAME:$LABEL" 
gcloud builds submit --tag gcr.io/typeworld2/$MACHINENAME:$LABEL

echo "Done."