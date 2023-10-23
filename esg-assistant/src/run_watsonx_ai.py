import json
from ibm_watson_machine_learning.foundation_models import Model

class WatsonxAI:

    def __init__(self, url, api_key, project_id ):
        self._credentials = { 
            "url"    : url, 
            "apikey" : api_key
        }
        self._project_id = project_id

    def set_model_parameters(self, model_id, gen_parameters):
        self._model_id = model_id
        self._gen_parameters = gen_parameters
        self._model = Model( model_id, self._credentials, self._gen_parameters, self._project_id )

    def generate(self, prompt ):
        
        generated_response = self._model.generate( prompt )

        if ( "results" in generated_response ) \
        and ( len( generated_response["results"] ) > 0 ) \
        and ( "generated_text" in generated_response["results"][0] ):
            return generated_response["results"][0]["generated_text"]
        else:
            print( "The model failed to generate an answer" )
            print( "\nDebug info:\n" + json.dumps( generated_response, indent=3 ) )
            return ""