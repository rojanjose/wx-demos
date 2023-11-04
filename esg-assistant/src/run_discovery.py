import re
import json
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

    def save_discovery_search(self, file_name, query_result):
        with open(file_name, "w") as outfile: 
            json.dump(query_result, outfile)


    def process_discovery_search(self, question, company):
        # Processing Setup
        count = 2
        max_per_document = 10
        passages = {
            "enabled": True,
            "per_document": True,
            "max_per_document": max_per_document,
            "fields": ['text', 'title'],
            "count": 10,
            "characters": "2000"
        }

        query_result = self._discovery.query(project_id=self._project_id, collection_ids=self._collection_ids, natural_language_query=question, count=count, passages=passages).get_result()
        
        # self.save_discovery_search("search_response.json", query_result)

        return query_result
    

    def print_project_and_collections(self):
        print(f"Project: {self._project_name}:{self._project_id}")
        print(f"Collections: {self._collection_name}:{self._collection_ids}" )



