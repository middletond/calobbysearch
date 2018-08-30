import requests
from service import settings

def message(text, attachments=None):
    """Send a message to slack using app settings."""
    response = requests.post(
        url=settings.SLACK_URL,
        data={
            "text": text,
            "attachments": attachments,
        }
    )
    if response.status_code != 200:
        reason = "{} {}".format(response.status_code, response.text)
        raise requests.HTTPError(reason)
    return response
