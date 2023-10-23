import os
import datetime
import json
from dotenv import load_dotenv

from run_discovery import WatsonDiscovery
from run_watsonx_ai import WatsonxAI

from ibm_watson_machine_learning.foundation_models.utils.enums import ModelTypes
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams
from ibm_watson_machine_learning.foundation_models.utils.enums import DecodingMethods
from ibm_watson_machine_learning.foundation_models import Model

#Global variables
discovery = None
watson_ai = None
companies = None
theme_discovery_file = "../data/prompts/theme_discovery_query2.txt"
theme_prompt_file = "../data/prompts/theme_mapping2.txt"
audience_discovery_file = "../data/prompts/audience_discovery_query.txt"
audience_prompt_file = "../data/prompts/audience_mapping1.txt"

discovery_query_file = {
    "theme-query-file": "../data/prompts/theme_discovery_query2.txt",
    "audience-query-file": "../data/prompts/audience_discovery_query.txt",
    "impacts-query-file": "../data/prompts/audience_discovery_query.txt"
}


def init():
    global discovery
    global watson_ai
    global companies

    load_dotenv()
    #Init discovery invoker
    discovery = WatsonDiscovery(os.getenv("WATSON_DISCOVERY_URL", None), 
                                os.getenv("WATSON_DISCOVERY_API_KEY", None))
    discovery.set_project_name(os.getenv("WATSON_DISCOVERY_PROJECT_NAME", None))
    discovery.set_collection_name(os.getenv("WATSON_DISCOVERY_COLLECTION_NAME", None))

    #Init Watsonx.ai invoker
    watson_ai = WatsonxAI(os.getenv("GENAI_API", None), 
                          os.getenv("GENAI_KEY", None), 
                          os.environ["PROJECT_ID"])
    model_id = ModelTypes.LLAMA_2_70B_CHAT
    parameters = {
        GenParams.DECODING_METHOD: DecodingMethods.GREEDY,
        GenParams.MIN_NEW_TOKENS: 1,
        GenParams.MAX_NEW_TOKENS: 500,
        GenParams.REPETITION_PENALTY: 1.2
    }
    watson_ai.set_model_parameters(model_id, parameters)

    #Initalize the list of companies
    companies = ["coke", "Apple", "Microsoft", "Ford", "Verizon", "WellsFargo", "Netflix", "Amazon"]
    # companies = ["coke"]


def get_prompt(prompt_file):
    with open(prompt_file) as prompt_file:
        theme_prompt = prompt_file.read()
    return theme_prompt

def augment(template_in, context_in ):
    return template_in % ( context_in )

def main():
    print("Initializing stage1 retrieval")
    init()

    #Run stage1 inference for each company
    for company in companies:
        print("\n==============================================")
        print(f"Mapping themes for {company}")
        theme_discovery_query = augment(get_prompt(theme_discovery_file), company)
        print(f"Discovery query: {theme_discovery_query}")
        # audience_discovery_query = augment(get_prompt(audience_discovery_file), company)
        # print(f"Discovery query: {audience_discovery_query}")

        # print(str(datetime.datetime.now()))
        relevant_passages = discovery.process_discovery_search(theme_discovery_query, company)
        # relevant_passages = discovery.process_discovery_search(audience_discovery_query, company)

        inference_file = open(f"../data/10K-inferences/{company}-10K-ESG-Themes.html", "w")
        inference_file.write(f"<html><head><meta name=\"description\" content=\"Themes extracted from 10K\"></head><body><h1>{company} ESG Themes from 10K</h1><div>")

        for passages in relevant_passages:
            inference_file.write(f"\nSource: {relevant_passages[passages]['source']}\n")
            passage_indexes = ['p1', 'p2', 'p3']
            for p_index in passage_indexes:
                passage = relevant_passages[passages][p_index]
                generated_prompt = augment(get_prompt(theme_prompt_file), passage)
                response = watson_ai.generate(generated_prompt)
                print(f"\nPassage:\n{passage} \nMapping:\n{response} \n----------------------------------------------\n")
                inference_file.write(f"\n{response}")
            inference_file.write("</div><div>")
            
        inference_file.write(f"</div></body></html>")
        inference_file.close()

        # print(str(datetime.datetime.now()))
        # for passage in relevant_passages:
        #     generated_prompt = augment(get_prompt(theme_prompt_file), passage)
        #     # generated_prompt = augment(get_prompt(audience_prompt_file), passage)
        #     print(f"\nGenerated prompt: {generated_prompt}")
        #     # print(f"Passage: {passage}")

        #     # print(str(datetime.datetime.now()))    
        #     response = watson_ai.generate(generated_prompt)
        #     # print(str(datetime.datetime.now()))
        #     print(f"\nResponse: {response}")
        #     # response_json = json.loads(response)
        #     # print(response_json['themes'])


if __name__ == "__main__":
    main()

    
    

