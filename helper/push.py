import json
from typing import Optional

import requests
from imgurpython import ImgurClient

import config

API_URL = config.API_URL


def push(project: str, level: str, message: str, img_path: Optional[str] = None):
    d = {
        "project": project,
        "level": level,
        "message": message,
    }
    if img_path:
        client = ImgurClient(config.IMGUR_CLIENT_ID, config.IMGUR_CLIENT_SECRET)
        uploaded_img = client.upload_from_path(img_path, config=None, anon=None)
        d["img_url"] = uploaded_img["link"]
    resp = requests.post(API_URL, json=d)
    return resp
