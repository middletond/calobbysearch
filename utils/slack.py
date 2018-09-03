import requests
from datetime import datetime

from service import settings as service_settings

DATETIME_FORMAT = "%b. %-d, %Y, %-I:%M%p"
USE_SHORT_FIELDS = True

def message(text, attachments=None):
    """Send a message to slack using app settings."""
    if not isinstance(attachments, (list, tuple)):
        attachments = [attachments]

    response = requests.post(service_settings.SLACK_URL, json={
        "text": text,
        "attachments": attachments,
    })
    if response.status_code != 200:
        reason = "{} {}".format(response.status_code, response.text)
        raise requests.HTTPError(reason)
    return response

def attachment(title, data, url=None):
    """Creates a slack attachment from key-value data."""
    def empty(value):
        return value is None or value is ""

    def to_attachment_field(key, value):
        if isinstance(value, datetime):
            value = value.strftime(DATETIME_FORMAT)
        return {
            "title": key.capitalize(),
            "value": value,
            "short": USE_SHORT_FIELDS,
        }
    return {
        "fallback": title,
        "title": title.capitalize(),
        "title_link": url,
        "fields": [to_attachment_field(key, val) for key, val in data.items() if not empty(val)]
    }
