from flask import Flask, request
from bot2 import Bot
import os
from r_model import curator
app = Flask(__name__)

DB = os.environ.get('DB')
DB_USER = os.environ.get('DB_USER')
DB_HOST = os.environ.get('DB_HOST')
DB_PW = os.environ.get('DB_PW')

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN')

bot = Bot(ACCESS_TOKEN)
curator_info=curator(DB, DB_USER, DB_HOST, DB_PW)

@app.route('/', methods=['GET', 'POST'])
def receive_message_get_curator():
    if request.method == 'GET':
        token_sent = request.args['hub.verify_token']
        return verify_fb_token(token_sent)
    else:
        output = request.get_json(force=True)
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    if message['message'].get('text'):
                        recipient_id = message['sender']['id']
                        text = message['message']['text']
                        receive_curator(recipient_id, text)
                        return 'Done'
    return 'OK'

def verify_fb_token(token_sent):
    '''Сверяет токен, отправленный фейсбуком, с имеющимся у вас.
    При соответствии позволяет осуществить запрос, в обратном случае выдает ошибку.'''
    if token_sent == VERIFY_TOKEN:
        print("Verified")
        return request.args['hub.challenge']
    else:
        print('wrong verification token')
        return 'Invalid verification token'

def receive_curator(recipient_id, text):
    send_message(recipient_id, curator_info.get_curator(text))
    return 'pass'

def send_message(recipient_id, response):
    '''Отправляет пользователю текстовое сообщение в соответствии с параметром response.'''
    bot.send_text_message(recipient_id, response)
    return 'Success'

if __name__ == '__main__':
    app.run()