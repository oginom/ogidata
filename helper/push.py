import json

import requests

import config

API_URL = config.API_URL


def push(project: str, level: str, message: str):
    d = {
        "project": project,
        "level": level,
        "message": message,
    }
    resp = requests.post(API_URL, json=d)
    return resp
