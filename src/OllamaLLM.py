import requests
import json

from typing import Iterator

class OllamaLLM():
    def __init__(self, port : int = 11434):
        with open("../resources/context.txt", "r", encoding="utf-8") as file:
            self.context = file.read()

        self.model_name = "llama3:8b-instruct-q8_0"
        self.show_thinking = False
        self.port = port
        self.subprocess = None

        self.model = None
        self.temperature = 0.1

        self.base_url = "http://localhost:11434"
        self.chat_url = self.base_url + "/api/chat"
        self.tag_url = self.base_url + "/api/tags"

        self._models_cache = {}

    
    def output_chat_stream(self, message : str) -> Iterator[str]:
        llm_input = [
            {"role" : "system", "content" : self.context},
            {"role" : "user", "content" : message}
        ]

        options = {
            "temperature" : self.temperature,
            "seed" : 194266
        }

        post_json = {
            "model" : self.model_name,
            "messages" : llm_input,
            "options" : options,
            "stream" : True
        }

        response = requests.post(
            self.chat_url,
            json=post_json,
            stream=True
        )

        # NOTE : 
        # line.decode("utf-8") returns:
        # {
        #     "model" : str,
        #     "message" : {
        #         "role" : str,
        #         "content" : str
        #     },
        #     "done" : bool
        # }
        for line in response.iter_lines():
            try:
                chunk = json.loads(line.decode("utf-8"))
                yield chunk["message"]["content"]

            except json.JSONDecodeError as e:
                print(f"[ERROR] JSON Error: {e}")
    
    # not used yet
    def get_available_models_ollama(self) -> None:
        response = requests.get(self.tag_url).json()

        print("Available models:")
        for model in response["models"]:
            print(f"{model['name']}")

        return

    def is_ollama_server_running(self) -> bool:
        try:
            requests.get(self.base_url)
            return True
        except:
            return False