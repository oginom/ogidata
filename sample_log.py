import json

import requests

url = "https://xxxx.run.app"


def log(project: str, level: str, message: str):
    d = {
        "project": project,
        "level": level,
        "message": message,
    }
    resp = requests.post(url, json=d)
    print(resp.code)
    print(resp.text)


if __name__ == "__main__":
    log("sample_project", "debug", "sample message")
