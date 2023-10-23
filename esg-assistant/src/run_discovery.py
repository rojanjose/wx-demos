import re
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from ibm_watson import DiscoveryV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


class WatsonDiscovery:

    def __init__(self, url, api_key):
        self._url = url
        self._api_key = api_key
        self._authenticator = IAMAuthenticator(api_key)
        self._discovery = DiscoveryV2(
            version='2020-08-30',
            authenticator=self._authenticator
        )
        self._discovery.set_service_url(url)

    # Set project variables
    def set_project_name(self, project_name):
        self._project_name = project_name
        self._project_id = ''
        projects = self._discovery.list_projects().get_result()
        for project in projects['projects']:
            # print("Project:", project)
            if (project['name'] == project_name):
                self._project_id = project['project_id']

    # Set Collection variables
    def set_collection_name(self, collection_name):   
        self._collection_name = collection_name   
        self._collection_ids = []
        collections = self._discovery.list_collections(project_id = self._project_id).get_result()
        for collection in collections['collections']:
            # print("Collection: ", collection)
            if (collection['name'] == collection_name):
                self._collection_ids.append( collection['collection_id'] )


    def format_string(self, passage):
        string_encode = passage.encode("ascii", "ignore")
        string_decode = string_encode.decode()
        clean_text = BeautifulSoup(string_decode, "lxml").text
        perfect_text = " ".join(clean_text.split())
        perfect_text = re.sub(' +', ' ', perfect_text).strip('"')

        return perfect_text


    def process_discovery_search(self, question, company):
        # Processing Setup
        print("quest_text: ", question)
        query_result = self._discovery.query(project_id=self._project_id, collection_ids=self._collection_ids, query=question).get_result()
        range_limit = len(query_result['results'])
        # print(f"Returned {range_limit} results.")
        
        #Process search results that has the company name in the file name
        # relevant_passages = []
        passage_count = 0
        relevant_passages = dict()
        for i in range(0, range_limit):
            file_name = query_result['results'][i]['extracted_metadata']['filename']
            if(company in file_name):
                # print(f"File: {file_name}")
                relevant_passages[f'passage_{passage_count}'] = {
                    "source": file_name,
                    "p1": self.format_string(query_result['results'][i]['document_passages'][0]['passage_text']),
                    "p2": self.format_string(query_result['results'][i]['document_passages'][1]['passage_text']),
                    "p3": self.format_string(query_result['results'][i]['document_passages'][2]['passage_text'])
                }

                # relevant_passages.append(self.format_string(query_result['results'][i]['document_passages'][0]['passage_text']))
                # relevant_passages.append(self.format_string(query_result['results'][i]['document_passages'][1]['passage_text']))
                # relevant_passages.append(self.format_string(query_result['results'][i]['document_passages'][2]['passage_text']))
                passage_count += 1

        return(relevant_passages)
    

    def print_project_and_collections(self):
        print(f"Project: {self._project_name}:{self._project_id}")
        print(f"Collections: {self._collection_name}:{self._collection_ids}" )



