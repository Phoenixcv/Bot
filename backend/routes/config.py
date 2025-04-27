import json
import os

CONFIG_FILE = os.path.join(os.path.dirname(__file__), '..', 'config.json')

def load_config():
    with open(CONFIG_FILE, 'r') as file:
        config = json.load(file)
    return config

def get_selected_symbols():
    config = load_config()
    return config.get('symbols', [])
