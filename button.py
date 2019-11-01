import json
import six
import requests
from pymessenger.graph_api import FacebookGraphApi
from pymessenger.bot import Bot
import pymessenger.utils as utils
from pymessenger.bot import Bot


class Button(FacebookGraphApi):

    def __init__(self, *args, **kwargs):
        super(Button, self).__init__(*args, **kwargs)

    def send_qr_message(self, recipient_id, text, buttons):
        '''Send text messages to the specified recipient.
        https://developers.facebook.com/docs/messenger-platform/send-api-reference/button-template
        Input:
            recipient_id: recipient id to send to
            text: text of message to send
            buttons: buttons to send
        Output:
            Response from API as <dict>
        '''

        payload = {
            'recipient': {
                'id': recipient_id
            },
            "messaging_type": "RESPONSE",
            'message': {
                "text": text,
                "quick_replies": buttons
            }
        }
        return self.send_raw(payload)

    def send_raw(self, payload):
        request_endpoint = '{0}/me/messages'.format(self.graph_url)
        response = requests.post(
            request_endpoint,
            params=self.auth_args,
            json=payload
        )
        result = response.json()
        return result
