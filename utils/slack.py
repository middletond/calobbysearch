import requests
from service import settings

def message(text, attachments=None):
    """Send a message to slack using app settings."""
    if not isinstance(attachments, (list, tuple)):
        attachments = [attachments]

    response = requests.post(
        url=settings.SLACK_URL,
        json={
            "text": text,
            "attachments": attachments,
        }
    )
    if response.status_code != 200:
        reason = "{} {}".format(response.status_code, response.text)
        raise requests.HTTPError(reason)
    return response

def attachment(title, data, url=None, short_fields=True):
    """Creates a slack attachment from key-value data."""
    def to_attachment_field(key, val):
        return {
            "title": key.capitalize(),
            "value": "High",
            "short": short_fields,
        }
    return {
        "fallback": title,
        "title": title.capitalize(),
        "title_link": url,
        "fields": [to_attachment_field(key, val) for key, val in data.items()]
    }

# {
# 	"text": "Testing headline",
#     "attachments": [
#         {
#             "fallback": "Required plain-text summary of the attachment.",
#             "color": "#36a64f",
#             "author_name": "Bobby Tables",
#             "author_link": "http://flickr.com/bobby/",
#             "author_icon": "http://flickr.com/icons/bobby.jpg",
#             "title": "Slack API Documentation",
#             "title_link": "https://api.slack.com/",
#             "text": "Optional text that appears within the attachment",
#             "fields": [
#                 {
#                     "title": "Priority",
#                     "value": "High",
#                     "short": true
#                 },
# 				 {
#                     "title": "Test",
#                     "value": "High",
#                     "short": true
#                 },
# 				{
#                     "title": "Test",
#                     "value": "High",
#                     "short": true
#                 }
#             ],
#             "image_url": "http://my-website.com/path/to/image.jpg",
#             "thumb_url": "http://example.com/path/to/thumb.png",
#             "footer": "Slack API",
#             "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
#             "ts": 123456789
#         }
#     ]
# }
