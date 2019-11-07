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

if __name__ == '__main__':
    app.run()

