# NOTE: you must set $API_KEY below using information retrieved from your IBM Cloud account 
# (https://dataplatform.cloud.ibm.com/docs/content/wsj/analyze-data/ml-authentication.html)

set -a # Automatically export all variables
source .env
set +a # Turn off auto-export

IAM_TOKEN=$(curl --insecure -X POST --header "Content-Type: application/x-www-form-urlencoded" --header "Accept: \
 application/json" --data-urlencode "grant_type=urn:ibm:params:oauth:grant-type:apikey" \
  --data-urlencode "apikey=${GENAI_KEY}" "${TOKEN_ENDPOINT}" | jq -r '.access_token')

# echo "Generated token: ${IAM_TOKEN}"

# Invoke prompt template using the generated token.
curl -X POST --header "Content-Type: application/json" --header "Accept: application/json" --header "Authorization: \
  Bearer ${IAM_TOKEN}" -d @-  ${GENERATE_ENDPOINT} < payload.json

