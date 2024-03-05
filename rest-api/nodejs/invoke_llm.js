
const qs = require('querystring');
require('dotenv').config();

async function getAccessToken() {
    try {

        const iamEndpoint = process.env.TOKEN_ENDPOINT;
        const apiKey = process.env.GENAI_KEY;
        
        const params = {
            'grant_type': 'urn:ibm:params:oauth:grant-type:apikey',
            'apikey': apiKey
        };
        
        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json'
            },
            body: qs.stringify(params)
        };

        const response = await fetch(iamEndpoint, options);
        const data = await response.json();

        if (data.access_token) {
            // console.log('Access Token:', data.access_token);
        } else {
            console.error('Failed to obtain access token:', data);
        }

        return data.access_token

    } catch (error) {
        console.error('Error fetching access token:', error);
    }
}


// export const generateText = async () => {
async function generateText(accessToken){

    const generateEndpoint = process.env.GENERATE_ENDPOINT;
	const headers = {
		"Accept": "application/json",
		"Content-Type": "application/json",
		"Authorization": "Bearer " + accessToken
	};

    console.log("Headers: ", headers)
    const payload = require('./payload.json');

    try {
        const response = await fetch(generateEndpoint, {
            headers,
            method: "POST",
            body: JSON.stringify(payload)
        });

        return await response.json();

    } catch (error) {
        console.error("Error generating LLM response:", error.response.data);
    }
}


async function runMain() {
    try {
        const accessToken = await getAccessToken();

        const response = await generateText(accessToken);

        console.log("Response:", response);

    } catch (error) {
        console.error("An error occurred:", error);
    }
}

runMain();
