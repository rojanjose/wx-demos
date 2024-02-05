import os
import re
import json

from dotenv import load_dotenv
from run_discovery import WatsonDiscovery

load_dotenv()
discovery = WatsonDiscovery(os.getenv("WATSON_DISCOVERY_URL", None), 
                            os.getenv("WATSON_DISCOVERY_API_KEY", None))



discovery.set_project_name("Help Docs")
discovery.set_collection_name("Knowledge Articles")
discovery.print_project_and_collections()

discovery.set_project_name("help.salesloft.com")
discovery.set_collection_name("Knowledge Articles")
discovery.print_project_and_collections()