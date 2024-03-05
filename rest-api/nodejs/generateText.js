const axios = require('axios');
const qs = require('qs');
require('dotenv').config();

async function getAccessToken() {

    const iamEndpoint = process.env.TOKEN_ENDPOINT;
    const apiKey = process.env.GENAI_KEY;
    
    const params = new URLSearchParams();
    params.append('grant_type', 'urn:ibm:params:oauth:grant-type:apikey');
    params.append('apikey', apiKey);

    try {
        const response = await axios.post(iamEndpoint, params, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        });

        console.log("Access Token:", response.data.access_token);
        return response.data.access_token;
    } catch (error) {
        console.error("Error getting access token:", error.response.data);
    }
}

async function generateText(accessToken) {

    const generateEndpoint = process.env.GENERATE_ENDPOINT;
    const headers = {
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + accessToken
        }
	};

    const payload = require('./payload.json');
    // console.log("Payload data is:\n", payload);

    console.log("Payload data is:\n", payload);

    try {
        const response = await axios.post(generateEndpoint, payload, headers);

        console.log("Response:", response.data.results[0].generated_text);
        return response.data;

    } catch (error) {
        console.error("Error generating LLM response:", error.response.data);
    }
}

async function runMain() {
    try {
        const accessToken = await getAccessToken();

        const response = await generateText(accessToken);

    } catch (error) {
        console.error("An error occurred:", error);
    }
}

runMain();


