#!/bin/sh

# GENAI_KEY=vD0NOdd-03m3o2mDmjdWxw10yK-wRboHJLKXDGkn3SOq
GENAI_KEY=dylrT7zJLlA2UMsoeUjc4WPPFVcKMHVtKNIkezknhSKC

# IAM_TOKEN=$(curl --insecure -X POST --header "Content-Type: application/x-www-form-urlencoded" --header "Accept: \
#  application/json" --data-urlencode "grant_type=urn:ibm:params:oauth:grant-type:apikey" \
#   --data-urlencode "apikey=${GENAI_KEY}" "https://iam.cloud.ibm.com/identity/token" | jq '.access_token')


curl --insecure -X POST --header "Content-Type: application/x-www-form-urlencoded" --header "Accept: \
 application/json" --data-urlencode "grant_type=urn:ibm:params:oauth:grant-type:apikey" \
  --data-urlencode "apikey=${GENAI_KEY}" "https://iam.cloud.ibm.com/identity/token"

echo "\n\n\n"

curl -X POST 'https://iam.cloud.ibm.com/identity/token' -H 'Content-Type: application/x-www-form-urlencoded' \
 -d "grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey=${GENAI_KEY}"


# curl "https://us-south.ml.cloud.ibm.com/ml/v1-beta/generation/text?version=2023-05-29" \
#   -H 'Content-Type: application/json' \
#   -H 'Accept: application/json' \
#   -H "Authorization: Bearer $IAM_TOKEN" \
#   -d '{
# 	"input": "Input: How many days are there in a year?\nOutput:",
# 	"parameters": {
# 		"decoding_method": "greedy",
# 		"max_new_tokens": 20,
# 		"min_new_tokens": 1,
# 		"stop_sequences": [],
# 		"repetition_penalty": 1
# 	},
# 	"model_id": "meta-llama/llama-2-70b-chat",
# 	"project_id": "c50067ea-4aac-486e-8994-9978d292424a",
# 	"moderations": {
# 		"hap": {
# 			"input": true,
# 			"output": true,
# 			"threshold": 0.5,
# 			"mask": {
# 				"remove_entity_value": true
# 			}
# 		}
# 	}
# }'