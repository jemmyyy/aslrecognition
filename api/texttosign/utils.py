import json
import os

def load_data(file_name):
    
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    file_name = os.path.join(SITE_ROOT, file_name)

    with open(file_name, "r", encoding='utf-8') as file:
        return json.load(file)