import json
import os

def load_metadata(api_name, base_path="data/metadata"):
    folder = os.path.join(base_path, api_name)
    with open(os.path.join(folder, "request.json")) as f:
        request = json.load(f)
    with open(os.path.join(folder, "response.json")) as f:
        response = json.load(f)
    with open(os.path.join(folder, "justification.txt")) as f:
        justification = f.read()
    return {"api_name": api_name, "request": request, "response": response, "justification": justification}
