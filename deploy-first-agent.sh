export GOOGLE_CLOUD_PROJECT=putti-argolis-1
export GOOGLE_CLOUD_LOCATION=asia-southeast1
export AGENT_PATH="my-first-agent/"
export SERVICE_NAME="first-agent-service"
export APP_NAME="my-first-agent"
export GOOGLE_GENAI_USE_VERTEXAI=True

adk deploy cloud_run \
--project=$GOOGLE_CLOUD_PROJECT \
--region=$GOOGLE_CLOUD_LOCATION \
--service_name=$SERVICE_NAME  \
--app_name=$APP_NAME \
--with_ui \
$AGENT_PATH