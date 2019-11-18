import random
from flask import Flask, request
from bot2 import Bot
from pymessenger import Element, Button
import os
import datetime
import json
import requests
import attr
from requests_toolbelt import MultipartEncoder

# import enum
# import pymessenger2
# from pymessenger2 import utils
# from pymessenger2.utils import AttrsEncoder

app = Flask(__name__)

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN')

bot = Bot(ACCESS_TOKEN)


# Получать сообщения, посылаемые фейсбуком нашему боту мы будем в этом терминале вызова
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
        output = request.get_json(force=True)
        f = open('logs.txt', 'a')
        f.write(str(output) + '\n')
        f.close()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('postback'):
                    recipient_id = message['sender']['id']
                    postback_body = message['postback']['payload']
                    receive_postback(recipient_id, postback_body)
                    return 'Done'
                elif message.get('text'):
                    recipient_id = message['sender']['id']
                    send_message(recipient_id, 'К сожалению, бот не воспринимает текстовые сообщения. Пожулйста, выбери один из доступных пунктов меню.')
                    return 'Done'
                elif message.get('attachments'):
                    recipient_id = message['sender']['id']
                    send_message(recipient_id, 'К сожалению, бот не воспринимает вложения, такие как картинки, видео и аудио и не может на них отвечать. Пожулйста, выбери один из доступных пунктов меню.')
                    return 'Done'
    return 'OK'

def receive_postback(recipient_id, postback_body):
    if postback_body == 'StarT':
        send_message(recipient_id,
                     'Привет, я помогу тебе разобраться с работой в мобильной платформе. Я пока еще не готов, но ты можешь почитать статью на Вики ЛМ: https://intraru3.leroymerlin.ru/wiki_page/article/ff37b167-2b02-ea11-80e7-3a9fa140007b?ref=/wiki_page/search?query=%D0%9C%D0%BE%D0%B1%D0%B8%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F')
        return 'pass'
    elif postback_body == 'wifi':
        send_video(recipient_id, "486693275268886")
        return 'pass'
    elif postback_body == 'createBV':
        send_video(recipient_id, "423349031937094")
        return 'pass'
    elif postback_body == 'recalRM':
        send_video(recipient_id, "773792666414661")
        return 'pass'
    elif postback_body == 'BVandservice':
        send_video(recipient_id, "2578299052263509")
        return 'pass'
    elif postback_body == 'changeBV':
        send_video(recipient_id, "503631150228565")
        return 'pass'
    elif postback_body == 'productInfo':
        send_video(recipient_id, "491717245055585")
        return 'pass'
    elif postback_body == 'subscribeClient':
        send_video(recipient_id, "1315002718685687")
        return 'pass'
    elif postback_body == 'honestInfo':
        send_video(recipient_id, "503975686855553")
        return 'pass'
    elif postback_body == 'configurateMail':
        send_video(recipient_id, "548599715975235")
        return 'pass'
    elif postback_body == 'Mobalytics':
        send_video(recipient_id, "547146826069273")
        return 'pass'
    elif postback_body == 'OhMyBoss':
        send_video(recipient_id, "480862626156448")
        return 'pass'
    elif postback_body == 'Otdel':
        send_video(recipient_id, "551432335425632")
        return 'pass'
    elif postback_body == 'clientApp':
        send_video(recipient_id, "810909466011156")
        return 'pass'
    elif postback_body == 'C3correction':
        send_video(recipient_id, "2704255672930630")
        return 'pass'
    elif postback_body == 'Dostovernost':
        send_video(recipient_id, "430998330918655")
        return 'pass'
    elif postback_body == 'suplyInfo':
        send_video(recipient_id, "583908779027614")
        return 'pass'
    elif postback_body == 'One':
        send_message(recipient_id, 'Видео с ютубчика https://www.youtube.com/watch?v=eqBZDHlYO70')
        return 'pass'
    elif postback_body == 'Two':
        send_image(recipient_id, 'https://i.ytimg.com/vi/pDGHtNlr4-4/maxresdefault.jpg')
        send_image(recipient_id, 'https://vtlya.github.io/datastorage/videos/wi_fi.png')
        return 'pass'
    else:
        send_message(recipient_id,
                     'Вы воспользовались недопустимой командой. Воспользуйтесь рабочим пунктом меню. Бот не воспринимает текстовые сообщения!')
        return 'pass'


#

# def delete_turn_file(recipient_id):
#    os.remove('/turn/' + recipient_id + '.json')


# def check_turn(recipient_id):
#    file_path = os.path.join('turn\\', recipient_id + '.json')
#    return os.path.exists(file_path)

# def create_turn_file(recipient_id):
#    file_path = os.path.join('turn\\', recipient_id + '.json')
#    turn_file = open(file_path, 'a')
#    turn_file.close()


# def get_curent_action(recipient_id):
#    file_path = os.path.join('turn\\', recipient_id + '.json')
#    with open(file_path, 'r') as f:
#        data = json.loads(f.read())
#        if 'action_name' in data:
#            action_name = data['action_name']
#            return action_name
#        else:
#            return 'Err'


# def get_curent_step(recipient_id, action_name):
#    file_path = os.path.join('turn\\', recipient_id + '.json')
#    with open(file_path, 'r') as f:
#        data = json.loads(f.read())
#        if action_name == 'NewPeopleRegistration':
#            if data['will_people'] == True:
#                curent_action = 'people_name'
#            else:
#                for key in data.keys():
#                    if data[key] == None:
#                        curent_action = str(key)
#                        break
#            return curent_action

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


def send_video(recipient_id, video_id):
    '''Отправка видосика'''
    bot.send_attachment_by_id(recipient_id, type='video', id=video_id)
    return 'video sent'


def send_image(recpient_id, image_url):
    bot.send_image_url(recpient_id, image_url)
    return 'image sent'


def send_local_image(recepient_id, image_path):
    bot.send_image(recepient_id, image_path)
    return 'local image sent'


# ef send_but(recipient_id, buts):
#    '''Отправляет кнопки'''
#    bot.send_button_message(recipient_id, "В какой раздел ты бы хотел перейти?", buts)
#    return 'Success'

if __name__ == '__main__':
    app.run()
