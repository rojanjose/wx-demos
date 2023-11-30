import os
from dotenv import load_dotenv

from ibm_watson_machine_learning.foundation_models import Model

def main():

    print("Setting credentials from the .env file")
    load_dotenv()
    credentials = {
		"url" : os.getenv("GENAI_API", None),
		"apikey" : os.getenv("GENAI_KEY", None)
	}

    project_id = os.getenv("PROJECT_ID", None)
    space_id = None

    model_id = "google/flan-ul2"
    parameters = {
        "decoding_method": "greedy",
        "max_new_tokens": 300,
        "min_new_tokens": 50,
        "repetition_penalty": 1.5
    }

    model = Model(
        model_id = model_id,
        params = parameters,
        credentials = credentials,
        project_id = project_id
        )
    
    prompt_input = """Summarize the following paragraph in 2 sentences

Input:
Hi Josh,

I would suggest a 1-hour call which will cover overview of the product features, which Andy can deliver. Please schedule the initial call, keeping in mind east coast time. We will discuss regular connects for feedback and/or queries after the initial meeting.

Kind regards,

Peter Joseph
Director, 
Product Engineering ABCLabs
7th Floor, Block A, Golf Links,
Bangalore -560021, Karnataka, INDIA
Mobile: 91-9831117436
E-mail: peter@abclabs.com

From: Josh Jenson <josh@pte.com>
Sent: 07 June 2023 21:40
To: peter@abclabs.com; H Hasan <hasan@abc.com>; Jerry Soch  <soch@pte.com>
Subject: Re: Product pitch

Thanks Peter,

Thanks for quick comeback. Are you going to schedule the initial call or do you want us to schedule it. Who should be invited ?

Do you plan to have a weekly/bi weekly call for feedback?


Regards,
Josh

Output:
Josh wants to know who should be on the call, who will schedule it and at what frequency. Peter responded saying that we should have a 1 hour call with Ravi and we can have a regular connect.

Input:
Hi Leslie, 
Yes, once the final deliverable is determined, we will share it with Ravi. However, Milestone 1 is not going to be our Beta release deliverable. We are still implementing the new APIs we want to have for Beta. So, I am guessing this is just to get Ravi started with product runtime container? We expect it will change a lot in next few weeks.

Best Regards,
Krista

Hi Krista and Scott, I understand we have very minor work left for milestone 1 features. Could you please share the final milestone 1 containers with Ravi so that he can build the beta/demo/preview environment for us? We're doing it this way instead of a regular beta. Thanks! Ravi,  moving forward shall we have a weekly chat to touch base?

Leslie C. Chen
Sr. Product Manager, The AI Company
Email: l.chen@theaico.com


Output:
"""

    print("Submitting summarization request using this input prompt: ")
    print(prompt_input)
    generated_response = model.generate_text(prompt=prompt_input)
    print("\nResponse: ")
    print(generated_response)




if __name__ == "__main__":
    main()

    
    

