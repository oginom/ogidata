import json
import logging
import urllib.request

import flask
import functions_framework

import config

TOKEN = config.TOKEN
USER_ID_OGINO = config.USER_ID_OGINO
SLACK_WEBHOOK_URL = config.SLACK_WEBHOOK_URL


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


@functions_framework.http
def hello_http(request: flask.Request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    request_text = request.get_data(as_text=True)
    request_json = request.get_json(silent=True)
    request_args = request.args

    is_line = "destination" in request_json and "events" in request_json

    is_api = (
        "project" in request_json
        and "level" in request_json
        and "message" in request_json
    )

    if is_line:
        for message_event in request_json["events"]:
            line_reply(message_event["replyToken"], message_event["message"]["text"])
        line_push(USER_ID_OGINO, request_text)

    if is_api:
        project = request_json["project"]
        level = request_json["level"]
        message = request_json["message"]
        text = f"[{level}] {project}\n{message}"
        if level in ["error", "info"]:
            line_push(USER_ID_OGINO, text)
        if level in ["error", "warn", "info", "debug"]:
            slack_notify(text)

    return {"statusCode": 200, "body": json.dumps({"result": "success"})}


def slack_notify(text):
    url = SLACK_WEBHOOK_URL
    headers = {
        "Content-Type": "application/json",
    }
    body = {
        "text": text,
    }

    req = urllib.request.Request(
        url, data=json.dumps(body).encode("utf-8"), method="POST", headers=headers
    )
    with urllib.request.urlopen(req) as res:
        logger.info(res.read().decode("utf-8"))


def line_push(to_id, text):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + TOKEN,
    }
    body = {
        "to": to_id,
        "messages": [
            {
                "type": "text",
                "text": text,
            }
        ],
    }

    req = urllib.request.Request(
        url, data=json.dumps(body).encode("utf-8"), method="POST", headers=headers
    )
    with urllib.request.urlopen(req) as res:
        logger.info(res.read().decode("utf-8"))


def line_reply(replyToken, text):
    url = "https://api.line.me/v2/bot/message/reply"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + TOKEN,
    }
    body = {
        "replyToken": replyToken,
        "messages": [
            {
                "type": "text",
                "text": text,
            }
        ],
    }

    req = urllib.request.Request(
        url, data=json.dumps(body).encode("utf-8"), method="POST", headers=headers
    )
    with urllib.request.urlopen(req) as res:
        logger.info(res.read().decode("utf-8"))
