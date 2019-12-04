import random
from flask import Flask, request, redirect, url_for
from bot2 import Bot
from pymessenger import Element, Button
import os
from r_model import curator
import datetime
import requests
import attr
from requests_toolbelt import MultipartEncoder

app = Flask(__name__)

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN')

DB = os.environ.get('DB')
DB_USER = os.environ.get('DB_USER')
DB_HOST = os.environ.get('DB_HOST')
DB_PW = os.environ.get('DB_PW')

bot = Bot(ACCESS_TOKEN)
curator_info = curator(DB, DB_USER, DB_HOST, DB_PW)


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
            print(output)
            for message in messaging:
                if message.get('postback'):
                    recipient_id = message['sender']['id']
                    postback_body = message['postback']['payload']
                    receive_postback(recipient_id, postback_body)
                    print('ps_id = ', recipient_id)
                    return 'Done'
                elif message.get('message'):
                    if message['message'].get('text') and not (message['message'].get('quick_reply')):
                        recipient_id = message['sender']['id']
                        text = message['message']['text']
                        receive_text_message(recipient_id, text)
                        print('ps_id = ', recipient_id)
                        return 'Done'
                    if message['message'].get('attachments'):
                        recipient_id = message['sender']['id']
                        send_message(recipient_id, 'К сожалению, бот не воспринимает аудио/видео фалы, стикеры/картинки и не может на них отвечать. Пожулйста, выбери один из доступных пунктов меню. Инструкция как воспользоваться меню ниже')
                        send_image_by_id(recipient_id, "735516596944436")
                        print('ps_id = ', recipient_id)
                        return 'Done'
                    if message['message'].get('quick_reply'):
                        recipient_id = message['sender']['id']
                        postback_body = message['message']['quick_reply']['payload']
                        receive_postback(recipient_id, postback_body)
                        print('ps_id = ', recipient_id)
                        return 'Done'
    return 'OK'


def receive_text_message(recipient_id, text):
    if text == 'Привет' or text == 'Здарова' or text == 'Добрый день' or text == 'Здарово' or text == 'привет' or text == 'здарова' or text == 'добрый день' or text == 'здарово' or text == 'ghbdtn' or text == 'Ghbdtn':
        send_message(recipient_id, 'И тебе привет! Я могу помочь тебе разобраться с Мобильной платформой, а именно поделиться инструкциями как использовать приложение, узнать свежую информацию по мобильной платформе, котнаткы куратора твоего магазина и что делать в случае проблем с телефоном. На инструкции ниже показано как получить доступ к моему меню.')
        send_image_by_id(recipient_id, "735516596944436")
        return 'pass'
    elif text == 'Пока' or text == 'gjrf' or text == 'Gjrf' or text == 'пока':
        send_message(recipient_id, 'До встречи!')
    elif text == 'Как дела?' or text == 'rfr ltkf&' or text == 'Как дела' or text == 'как дела' or text == 'как дела?':
        send_message(recipient_id, 'Отлично! Надеюсь у тебя еще лучше 😉')
    elif is_digit(text) and (2 <= int(text) <= 176):
        receive_curator(recipient_id, text)
    else:
        send_message(recipient_id, "Я немогу распознать, что здесь написано:(\nПожалуйста, выбери нужный тебе пункт меню. Инструкция как открыть меню в картинке ниже:")
        send_image_by_id(recipient_id, "735516596944436")
        return 'pass'


def receive_postback(recipient_id, postback_body):
    if postback_body == 'StarT':
        send_message(recipient_id, 'Привет! Я могу помочь тебе разобраться с Мобильной платформой, а именно поделиться инструкциями как использовать приложение, узнать свежую информацию по мобильной платформе, котнаткы куратора твоего магазина и что делать в случае проблем с телефоном. На инструкции ниже показано как получить доступ к моему меню.')
        send_image_by_id(recipient_id, "735516596944436")
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
    elif postback_body == 'getsmart':
        send_message(recipient_id, "Каждый сотрудник Леруа Мерлен должен получить корпоративный смартфон в течении недели после принятия на работу. Для оформления заявки на выдачу смартфона можно обратиться к своему руководителю, либо куратору мобильной платформы. Также заявку можно оформить на портале ITSM самостоятельно, прейдя по ссылке и следуя инструкции с картинке ниже.")
        send_message(recipient_id, "Ссылка на портал ITSM: https://itsm.leroymerlin.ru/")
        send_image_by_id(recipient_id, "1229740157210291")
        return 'pass'
    elif postback_body == 'apps':
        send_message(recipient_id, 'Набор из 15 приложений, который устанавливается всем и которые невозможно удалить, '
                                   'включает в себя:\n1. IT Help - контакты IT\n2. Leroy Merlin - приложение '
                                   'клиента\n3. Магазин mobile - Основное приложение для продажи. В меню "обучения" '
                                   'бота можно найти видеоинструкции по каждому дейтсвию, которое можно совершить в '
                                   'этом приложение.\n4. OhMyBoss - приложение для опросов сотрудников.\n5. '
                                   'SuccessFactors (Web) - корпоративный портал для обучений.\n6 и 7. Workplace и '
                                   'Workchat - наша корпоративная соц. сеть и чат, соответсвенно.\n8. Вики ЛМ - ссылка '
                                   'на нашу корпоративную "википедию".  Здесь можно узнать значение терминов и '
                                   'формулировок, которые у нас используются.\n9. Интрару - наш корпоративный портал. '
                                   'Здесь можно запланировать командировку, отпуск и свой график. Получить доступ к '
                                   'оформлению социальных льгот, узнать детализацую начислений зп и многое '
                                   'другое.\n10. Достоверность - позволяет работать с достоверностью товарного '
                                   'запаса.\n11. Коррекция стока - позволяет скорректировать сток C3.\n12. Управление '
                                   'отделом - ежедневная отработка задач по артикулам для уменьшения аномалий '
                                   'запаса.\n13. Центр приложений - позволяет включить режим "Не на работе", '
                                   'который отклоняет все входящие звонки, установить дополнительные приложения, '
                                   'которые потенциально могут помочь в работе. Иногда отправляет уведомления для всех '
                                   'о различных событиях.\n14. Услуги LMKZ(только для казахстана) - ссылка на страницу '
                                   'услуг на сайте leroymerlin.kz\n15.Knox manage - позволяет установить дполнительные '
                                   'корпоративные приложения для работы, а также защищает телефон')
        send_message(recipient_id, 'Приложения ниже также используются для работы у нас в компании, некоторые из них '
                                   'публичные. Их возможно удалять. Изначально они не устанавливаются, но могут быть '
                                   'установленны через приложение Knox manage, следуя инструкции на картинке ниже.')
        send_image_by_id(recipient_id, "494079367985231")
        send_image_by_id(recipient_id, "772924719800076")
    elif postback_body == 'curator_info':
        send_message(recipient_id, 'Чтобы узнать, кто является куратором мобильной платформы, введи номер своего магазина.\nТвое сообщение не должно содержать посторонних символов, кроме номера магазина. Например:29')
        return 'pass'
    else:
        print('Cant recognize postback. Invalid postback')
        send_message(recipient_id, 'Выбранная возможность, к сожалению, пока не реализована. Она появиться как только будет возможно 😉')
        return 'pass'


def is_digit(string):
    if string.isdigit():
        return True
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False


def receive_curator(recipient_id, text):
    send_message(recipient_id, curator_info.get_curator(text))
    return 'pass'


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


def send_image_by_id(recipient_id, image_id):
    '''Отправка видосика'''
    bot.send_attachment_by_id(recipient_id, type='image', id=image_id)
    return 'video sent'


def send_local_image(recepient_id, image_path):
    bot.send_image(recepient_id, image_path)
    return 'local image sent'


if __name__ == '__main__':
    app.run()
