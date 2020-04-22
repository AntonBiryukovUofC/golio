import json
import os

with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.json')) as f:
    config = json.load(f)


def get():
    return config
