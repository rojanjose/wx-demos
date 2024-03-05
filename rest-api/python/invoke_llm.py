import requests
import json
import os
from dotenv import load_dotenv

class ModelInference:

    def __init__(self):
        # Load the .env file
        load_dotenv()

        self.api_key = os.environ["GENAI_KEY"]
        self.token_endpoint = os.environ["TOKEN_ENDPOINT"]
        self.generate_endpoint = os.environ["GENERATE_ENDPOINT"]
        self.access_token = ""

        # Read payload file
        payload_file_path = os.environ["PAYLOAD_FILE"]

        with open(payload_file_path, 'r') as file:
            self.payload = json.load(file)

    # Get API access token using the API key
    def get_token(self):

        # Headers and data for the POST request
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json"
        }
        data = {
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
            "apikey": self.api_key
        }

        response = requests.post(
	                        self.token_endpoint,
	                        headers=headers,
	                        data=data
                            )
        
        # Get access token, if the request was successful
        if response.status_code == 200:
            self.access_token = response.json().get("access_token")
            return self.access_token
        else:
            print(f"Error getting access token: {response.text}")
            return None

    # Invoke LLM to generate the CSV file
    def generate_text(self):

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.access_token
        }

        response = requests.post(
            self.generate_endpoint,
            headers=headers,
            json=self.payload
        )

        if response.status_code != 200:
            raise Exception("Non-200 response: " + str(response.text))

        data = response.json()
        
        return data.get("results")[0].get("generated_text")


    def display_values(self):
        print(f"API Key : {self.api_key}")
        print(f"Token : {self.token_endpoint}")
        print(f"Endpoint : {self.generate_endpoint}")


def main():

    generator = ModelInference()
    generator.get_token()
    model_response = generator.generate_text()
    print(f"Model response: \n{model_response}")


if __name__ == "__main__":
    main()



