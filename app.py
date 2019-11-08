import random
from flask import Flask, request
from pymessenger.bot import Bot
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
                if message.get('message'):
                    recipient_id = message['sender']['id']
                if message.get('postback'):
                    postback_body = message['postback']['payload']
                    receive_postback(recipient_id, postback_body)
    return 'OK'


def receive_postback(recipient_id, postback_body):
    if postback_body == 'StarT':
        send_message(recipient_id, 'Привет, я помогу тебе разобраться с работой в мобильной платформе + link_help')
    elif postback_body == 'MagMobile':
        send_message(recipient_id, 'ОБУЧЕНИЕ ПО МАГАЗИНУ')
        if check_turn(recipient_id) == True:
            delete_turn_file(recipient_id)
    elif postback_body == 'Dostovernost':
        send_message(recipient_id, 'https://vimeo.com/371585412/df8536a91e')
        if check_turn(recipient_id) == True:
            delete_turn_file(recipient_id)
    elif postback_body == 'One':
        send_message(recipient_id, 'Видео с ютубчика https://www.youtube.com/watch?v=eqBZDHlYO70')
    elif postback_body == 'Twor':
        send_message(recipient_id, 'Просто слова')
    else:
        send_message(recipient_id, 'Воспользуйтесь меню. ..Инструкция по меню.. .')


def check_turn(recipient_id):
    file_path = os.path.join('turn\\', recipient_id + '.json')
    return os.path.exists(file_path)


def delete_turn_file(recipient_id):
    os.remove('/turn/' + recipient_id + '.json')


def create_turn_file(recipient_id):
    file_path = os.path.join('turn\\', recipient_id + '.json')
    turn_file = open(file_path, 'a')
    turn_file.close()


def get_curent_action(recipient_id):
    file_path = os.path.join('turn\\', recipient_id + '.json')
    with open(file_path, 'r') as f:
        data = json.loads(f.read())
        if 'action_name' in data:
            action_name = data['action_name']
            return action_name
        else:
            return 'Err'


def get_curent_step(recipient_id, action_name):
    file_path = os.path.join('turn\\', recipient_id + '.json')
    with open(file_path, 'r') as f:
        data = json.loads(f.read())
        if action_name == 'NewPeopleRegistration':
            if data['will_people'] == True:
                curent_action = 'people_name'
            else:
                for key in data.keys():
                    if data[key] == None:
                        curent_action = str(key)
                        break
            return curent_action


def check_messege(curent_action, curent_step, text_message, recipient_id):
    if curent_action == 'NewPeopleRegistration':
        if curent_step == 'start_date':
            try:
                datetime.datetime.strptime(text_message, '%d.%m.%Y')
                return {'check': True, 'check_value': text_message}
            except:
                return {'check': False}
        elif curent_step == 'company_name':
            if len(text_message) >= 1 and len(text_message) <= 149:
                return {'check': True, 'check_value': text_message}
            else:
                return {'check': False}
        elif curent_step == 'people_name':
            if text_message == '':
                return {'check': False}
            else:
                return {'check': True, 'check_value': text_message}
        elif curent_step == 'will_people':
            if text_message.replace(' ', '') in {'Да', 'Да.', 'да', 'да.'}:
                return {'check': True, 'check_value': True}
            if text_message.replace(' ', '') in {'Нет', 'Нет.', 'нет', 'нет.'}:
                return {'check': True, 'check_value': False}
            else:
                return {'check': False}
        elif curent_step == 'replay':
            if text_message.replace(' ', '') in {'Да', 'Да.', 'да', 'да.'}:
                return {'check': True, 'check_value': True}
            if text_message.replace(' ', '') in {'Нет', 'Нет.', 'нет', 'нет.'}:
                return {'check': True, 'check_value': False}
            else:
                return {'check': False}
        elif curent_step == 'type':
            if text_message in {'1', '1 - По дням недели', 'По дням недели'}:
                return {'check': True, 'check_value': '1'}
            if text_message in {'2', '2 - По числам месяца', 'По числам месяца'}:
                return {'check': True, 'check_value': '2'}
            else:
                return {'check': False}
        elif curent_step == 'type_details':
            file_path = os.path.join('turn\\', recipient_id + '.json')
            with open(file_path, "r") as jsonFile:
                data = json.load(jsonFile)
            type = data['type']
            text_message = text_message.replace(' ', '')
            if type == '1':
                if ',' in text_message:
                    fake_day_flag = False
                    for day in text_message.split(','):
                        if day not in ['1', '2', '3', '4', '5', '6', '7']:
                            fake_day_flag = True
                    if fake_day_flag:
                        return {'check': False}
                    else:
                        return {'check': True, 'check_value': text_message}
                elif '-' in text_message:
                    if len(text_message.split('-')) == 2:
                        start_day = text_message.split('-')[0]
                        end_day = text_message.split('-')[1]
                        if start_day in ['1', '2', '3', '4', '5', '6'] and end_day in ['2', '3', '4', '5', '6', '7']:
                            try:
                                start_day_int = int(start_day)
                                end_day_int = int(end_day)
                                if start_day_int <= end_day_int:
                                    text_message = ''
                                    for day in range(start_day_int, end_day_int + 1):
                                        text_message += str(day) + ';'
                                    return {'check': True, 'check_value': text_message[:-1]}
                                else:
                                    return {'check': False}
                            except:
                                return {'check': False}
                        else:
                            return {'check': False}
                elif text_message in ['1', '2', '3', '4', '5', '6', '7']:
                    return {'check': True, 'check_value': text_message}
                elif text_message not in ['1', '2', '3', '4', '5', '6', '7']:
                    return {'check': False}
            if type == '2':
                day_dict = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16',
                            '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
                if ',' in text_message:
                    fake_day_flag = False
                    for day in text_message.split(','):
                        if day not in day_dict:
                            fake_day_flag = True
                    if fake_day_flag:
                        return {'check': False}
                    else:
                        return {'check': True, 'check_value': text_message}
                elif '-' in text_message:
                    if len(text_message.split('-')) == 2:
                        start_day = text_message.split('-')[0]
                        end_day = text_message.split('-')[1]
                        if start_day in day_dict and end_day in day_dict:
                            try:
                                start_day_int = int(start_day)
                                end_day_int = int(end_day)
                                if start_day_int < end_day_int:
                                    text_message = ''
                                    for day in range(start_day_int, end_day_int + 1):
                                        text_message += str(day) + ';'
                                    return {'check': True, 'check_value': text_message[:-1]}
                                else:
                                    return {'check': False}
                            except:
                                return {'check': False}
                        else:
                            return {'check': False}
                elif text_message in day_dict:
                    return {'check': True, 'check_value': text_message}
                elif text_message not in day_dict:
                    return {'check': False}
        elif curent_step == 'end_date':
            file_path = os.path.join('turn\\', recipient_id + '.json')
            with open(file_path, "r") as jsonFile:
                data = json.load(jsonFile)
            start_date = data['start_date']
            try:
                if datetime.datetime.strptime(text_message, '%d.%m.%Y') > datetime.datetime.strptime(start_date,
                                                                                                     '%d.%m.%Y'):
                    return {'check': True, 'check_value': text_message}
                else:
                    return {'check': False}
            except:
                return {'check': False}
        elif curent_step == 'approve':
            if text_message.replace(' ', '') in {'Да', 'Да.', 'да', 'да.'}:
                return {'check': True, 'check_value': True}
            if text_message.replace(' ', '') in {'Нет', 'Нет.', 'нет', 'нет.'}:
                return {'check': True, 'check_value': False}
            else:
                return {'check': False}


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


def send_but(recipient_id, buts):
    '''Отправляет кнопки'''
    bot.send_button_message(recipient_id, "В какой раздел ты бы хотел перейти?", buts)
    return 'Success'


if __name__ == '__main__':
    app.run()
