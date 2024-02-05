import os
import re
import json

from dotenv import load_dotenv
from run_discovery import WatsonDiscovery

#Global variables
discovery = None


def init():
    global discovery
    global log_file

    load_dotenv()
    #Init discovery invoker
    discovery = WatsonDiscovery(os.getenv("WATSON_DISCOVERY_URL", None), 
                                os.getenv("WATSON_DISCOVERY_API_KEY", None))
    discovery.set_project_name(os.getenv("WATSON_DISCOVERY_PROJECT_NAME", None))
    discovery.set_collection_name(os.getenv("WATSON_DISCOVERY_COLLECTION_NAME", None))

    log_file = open(f"./upload_docs.log", "w")

    

def extract_lines(input, start, end):
    extracted_lines = []
    copy = False
    for line in input.splitlines():
        if re.search(start, line) :
            copy = True
            continue
        elif re.search(end, line):
            copy = False
            continue
        elif copy and line != "\n":
            extracted_lines.append(line)

    return extracted_lines

def getFileMetadata(file_name, base_url):

    file_metadata = {}

    if( "topic" in file_name):
        file_metadata["content_type"] = "topic"
        file_metadata["filename"] = file_name.split("topic_",1)[1]
        matched_string = re.search('topic_(.*?)_', file_name )
        if matched_string:
            file_metadata["id"] = matched_string.group(1)
        else:
            file_metadata["id"] = "Unknown"

        matched_string = re.search(f'{file_metadata["id"]}_(.*?).html', file_name )
        if matched_string:
            extracted_string = matched_string.group(1)
            file_metadata["topic"] = ' '.join(word.capitalize() for word in extracted_string.split('_'))
        else:
            file_metadata["topic"] = 'Unknown'

        file_metadata["url"] = f"{base_url}/{file_metadata['content_type']}/{file_metadata['id']}/{extracted_string}"

    elif( "article" in file_name):
        file_metadata["content_type"] = "article"
        file_metadata["filename"] = file_name.split("article_",1)[1]

        matched_string = re.search(f'article_(.*?).html', file_name )
        if matched_string:
            extracted_string = matched_string.group(1)
            file_metadata["topic"] = ' '.join(word.capitalize() for word in extracted_string.split('_'))
        else: 
            file_metadata["topic"] = 'Unknown'

        file_metadata["url"] = f"{base_url}/{file_metadata['content_type']}/{extracted_string}"

    else:
        file_metadata["content_type"] = "unknown"
        file_metadata["filename"] = file_name
        file_metadata["id"] = "not defined"

    return file_metadata


def main():
    print("Initializing upload routine...")
    init()
    discovery.print_project_and_collections()

    log_file.write("Stating the upload process...")
    

    base_url = "https://help.salesloft.com/s/"
    scrape_dir = "../scrapper/scraped-pages"
    file_content_type = "text/html"

    toc_file_path = f'{scrape_dir}/toc.json'

    # Open the JSON file and load its content into a dictionary
    with open(toc_file_path, 'r') as file:
        toc = json.load(file)

    for file_metadata in toc:
        
        file_path = os.path.join(scrape_dir, file_metadata["filename"])
        # print("File meta: ", file_metadata)

          # Check if it's a file and not a directory
        if os.path.isfile(file_path):
            
            print("Adding document: ", file_path)
            upload_result = discovery.upload_document(discovery._collection_ids[0], file_path, file_metadata['filename'], file_content_type, json.dumps(file_metadata))
            print("Document upload result: ", upload_result)
        
    
    print("Document upload complete.")
    log_file.close()


if __name__ == "__main__":
    main()

    
    

