import json

import requests

url = "https://xxxx.run.app"


def push(project: str, level: str, message: str):
    d = {
        "project": project,
        "level": level,
        "message": message,
    }
    resp = requests.post(url, json=d)
    print(resp.status_code)
    print(resp.text)
