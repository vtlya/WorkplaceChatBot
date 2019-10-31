import random
from flask import Flask, request
from pymessenger.bot import Bot
from pymessenger import Element, Button
import os
import json
import requests
from schematics import Model
from schematics.types import StringType, ListType, PolyModelType, BooleanType
from fbotics.models.buttons import PostbackButton, WebUrlButton, CallButton
from fbotics.models.attachment import Attachment
from fbotics.models.message import Message
import attr
from requests_toolbelt import MultipartEncoder
#import enum
#import pymessenger2
#from pymessenger2 import utils
#from pymessenger2.utils import AttrsEncoder


app = Flask(__name__)

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN')

bot = Bot(ACCESS_TOKEN)

#Получать сообщения, посылаемые фейсбуком нашему боту мы будем в этом терминале вызова
@app.route('/', methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
    # до того как позволить людям отправлять что-либо боту, Facebook проверяет токен,
    # подтверждающий, что все запросы, получаемые ботом, приходят из Facebook
        token_sent = request.args['hub.verify_token']
        return verify_fb_token(token_sent)
    # если запрос не был GET, это был POST-запрос и мы обрабатываем запрос пользователя
    else:
        # получаем сообщение, отправленное пользователем для бота в Facebook
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                #определяем ID, чтобы знать куда отправлять ответ
                    recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    #response_sent_text = get_message()
                    send_button_template(recipient_id,user_ref="",phone_number="+7 926 7268690",text="call me",quick_replies=Qbuts1)
                    send_message(recipient_id, "Поулил сообщение")
                    send_message(recipient_id, "Вторая отправка для теста")
                    #send_quick_reply(recipient_id,"Выбери что-нибудь")
                    #send_but(recipient_id, Qbuts1)
                #если пользователь отправил GIF, фото, видео и любой не текстовый объект
                if message['message'].get('attachments'):
                    response_sent_nontext = get_message()
                    send_message(recipient_id, "Другой кейс для проверки условия когда сообщение не текстовое")
        return "Message Processed"

def verify_fb_token(token_sent):
    '''Сверяет токен, отправленный фейсбуком, с имеющимся у вас.
    При соответствии позволяет осуществить запрос, в обратном случае выдает ошибку.'''
    if token_sent == VERIFY_TOKEN:
        print("Verified")
        return request.args['hub.challenge']
    else:
        print('wrong verification token')
        return 'Invalid verification token'

def send_message(recipient_id, response):
    '''Отправляет пользователю текстовое сообщение в соответствии с параметром response.'''
    bot.send_text_message(recipient_id, response)
    return 'Success'

def send_but(recipient_id,buts):
    '''Отправляет кнопки'''
    bot.send_button_message(recipient_id, "В какой раздел ты бы хотел перейти?", buts)
    return 'Success'

def get_message():
    '''Отправляет случайные сообщения пользователю.'''
    sample_responses = ["Потрясающе!", "Я вами горжусь!", "Продолжайте в том же духе!", "Лучшее, что я когда-либо видел!"]
    return random.choice(sample_responses)

def get_started(self):
    payload = {
        "get_started": {
        "payload": "<postback_payload>"
        }
    }
    headers = {'Content-type': 'application/json'}
    URL = "https://graph.workplace.com/v2.6/me/messenger_profile?access_token=" + ACCESS_TOKEN #173.252.127.33
    r = requests.post(URL + "/session", json=payload)
    return print("Status: " + str(r.status_code), "/r Body: " + str(r.content))

def send_button_template(
    self,
    recipient_id=None,
    user_ref=None,
    phone_number=None,
    text=None,
    quick_replies=None,
    buttons=None,
):
    """Sends a button template to the recipient.

    # Arguments
    recipient_id: page specific id of the recipient
    user_ref: optional. user_ref from the checkbox plugin
    phone_number: Optional. Phone number of the recipient with the format +1(212)555-2368. Your bot must be approved for Customer Matching to send messages this way.
    text: UTF-8-encoded text of up to 640 characters. Text will appear above the buttons.
    quick_replies: An array of objects the describe the quick reply buttons to send. A maximum of 11 quick replies are supported.
    buttons: Set of 1-3 buttons that appear as call-to-actions.
    """

    button_template_payload = ButtonTemplatePayload(
        dict(template_type="button", text=text, buttons=buttons)
    )
    attachment = Attachment(dict(type="template", payload=button_template_payload))
    message = Message({"quick_replies": quick_replies, "attachment": attachment})
    response = self._post(message, recipient_id, user_ref, phone_number)
    return response
if __name__ == '__main__':
    app.run()

def button_claim_function(field, data):
    print("data", data)
    if "url" in data:
        return WebUrlButton
    if "payload" in data and data.get("type") == "postback":
        return PostbackButton
    if "payload" in data and data.get("type") == "phone_number":
        return CallButton
    else:
        return None


class ButtonTemplatePayload(Model):
    """The button template allows you to send a structured message that includes text and buttons.

    # Arguments
        template_type: Value must be button.
        text: UTF-8-encoded text of up to 640 characters. Text will appear above the buttons.
        buttons: Set of 1-3 buttons that appear as call-to-actions.
        sharable: Optional. Set to true to enable the native share button in Messenger for the template message. Defaults to false.

    """

    template_type = StringType(required=True, default="button", choices=["button"])
    text = StringType(required=True, max_length=640)
    buttons = ListType(
        PolyModelType(
            [PostbackButton, WebUrlButton, CallButton],
            claim_function=button_claim_function,
        )
    )
    sharable = BooleanType(default=False)

Qbuts1=[
    {
        "content_type":"text",
        "title":"Test qp",
        "payload":"<POSTBACK_PAYLOAD>",
        "image_url":"https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Leroy_Merlin.svg/800px-Leroy_Merlin.svg.png",
    }
    ]






'''
#new
def test_button_message():
    buttons = []
    button = PostbackButton(title='I button and i work', payload='other')
    buttons.append(button)
    #button = URLButton(title='Arsenal', url='http://arsenal.com')
    #buttons.append(button)
    text = 'Select'
    result = bot.send_button_message(recipient_id, text, buttons)
    assert type(result) is dict
    assert result.get('message_id') is not None
    assert result.get('recipient_id') is not None

@attr.s
class PostbackButton(object):
    """
    See https://developers.facebook.com/docs/messenger-platform/send-api-reference/postback-button
    """
    title = attr.ib()
    payload = attr.ib(default=None)
    type = attr.ib(default='postback')

    def __attrs_post_init__(self):
        assert self.type == 'postback', 'Type of a button can\'t be set ' \
                                        'manually.'
        if not self.payload:
            self.payload = self.title

'''

'''
def test_wrong_format_message():
    result = bot.send_text_message(recipient_id, {'text': "its a test"})
    assert type(result) is dict
    assert result.get('message_id') is None


def test_text_message():
    result = bot.send_text_message(recipient_id, "test")
    assert type(result) is dict
    assert result.get('message_id') is not None
    assert result.get('recipient_id') is not None


def test_elements():
    image_url = 'https://lh4.googleusercontent.com/-dZ2LhrpNpxs/AAAAAAAAAAI/AAAAAAAA1os/qrf-VeTVJrg/s0-c-k-no-ns/photo.jpg'
    elements = []
    element = Element(
        title="Arsenal",
        image_url=image_url,
        subtitle="Click to go to Arsenal website.",
        item_url="http://arsenal.com")
    elements.append(element)
    result = bot.send_generic_message(recipient_id, elements)
    assert type(result) is dict
    assert result.get('message_id') is not None
    assert result.get('recipient_id') is not None


def test_image_url():
    image_url = 'https://lh4.googleusercontent.com/-dZ2LhrpNpxs/AAAAAAAAAAI/AAAAAAAA1os/qrf-VeTVJrg/s0-c-k-no-ns/photo.jpg'
    result = bot.send_image_url(recipient_id, image_url)
    assert type(result) is dict
    assert result.get('message_id') is not None
    assert result.get('recipient_id') is not None


def test_image_gif_url():
    image_url = 'https://media.giphy.com/media/rl0FOxdz7CcxO/giphy.gif'
    result = bot.send_image_url(recipient_id, image_url)
    assert type(result) is dict
    assert result.get('message_id') is not None
    assert result.get('recipient_id') is not None


def test_mp3_url():
    mp3_url = 'https://archive.org/download/testmp3testfile/mpthreetest.mp3'
    result = bot.send_audio_url(recipient_id, mp3_url)
    assert type(result) is dict
    assert result.get('message_id') is not None
    assert result.get('recipient_id') is not None

def test_upload_mp3_file(tmpdir):
    mp3_url = 'https://archive.org/download/testmp3testfile/mpthreetest.mp3'
    f = tmpdir.join('mpthreetest.mp3')
    f.write_binary(requests.get(mp3_url).content)
    result = bot.send_audio(recipient_id, str(f))
    assert type(result) is dict
    assert result.get('message_id') is not None
    assert result.get('recipient_id') is not None

def test_button_message():
    buttons = []
    button = PostbackButton(title='Other', payload='other')
    buttons.append(button)
    #button = URLButton(title='Arsenal', url='http://arsenal.com')
    #buttons.append(button)
    text = 'Select'
    result = bot.send_button_message(recipient_id, text, buttons)
    assert type(result) is dict
    assert result.get('message_id') is not None
    assert result.get('recipient_id') is not None

def test_quick_reply():
    buttons = []
    button = QuickReply(content_type='text', title='Button 1', payload='btn1')
    buttons.append(button)
    button = QuickReply(content_type='text', title='Button 2', payload='btn2')
    buttons.append(button)
    message = 'Select'
    result = bot.send_quick_reply(recipient_id, message, buttons)
    assert type(result) is dict
    assert result.get('message_id') is not None
    assert result.get('recipient_id') is not None


def test_fields_blank():
    user_profile = bot.get_user_info(recipient_id)
    assert user_profile is not None


def test_fields():
    fields = ['first_name', 'last_name']
    user_profile = bot.get_user_info(recipient_id, fields=fields)
    assert user_profile is not None
    assert len(user_profile.keys()) == len(fields)




@attr.s
class PostbackButton(object):
    """
    See https://developers.facebook.com/docs/messenger-platform/send-api-reference/postback-button
    """
    title = attr.ib()
    payload = attr.ib(default=None)
    type = attr.ib(default='postback')

    def __attrs_post_init__(self):
        assert self.type == 'postback', 'Type of a button can\'t be set ' \
                                        'manually.'
        if not self.payload:
            self.payload = self.title
'''