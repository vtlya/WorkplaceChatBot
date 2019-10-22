import random
from flask import Flask, request
from pymessenger.bot import Bot
import os

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
                    response_sent_text = test_button_message()
                    send_message(recipient_id, response_sent_text)
                #если пользователь отправил GIF, фото, видео и любой не текстовый объект
                if message['message'].get('attachments'):
                    response_sent_nontext = get_message()
                    send_message(recipient_id, response_sent_nontext)
        return "Message Processed"

def verify_fb_token(token_sent):
    '''Сверяет токен, отправленный фейсбуком, с имеющимся у вас.
    При соответствии позволяет осуществить запрос, в обратном случае выдает ошибку.'''
    if token_sent == VERIFY_TOKEN:
        return request.args['hub.challenge']
    else:
        return 'Invalid verification token'

def send_message(recipient_id, response):
    '''Отправляет пользователю текстовое сообщение в соответствии с параметром response.'''
    bot.send_text_message(recipient_id, response)
    return 'Success'

def get_message():
    '''Отправляет случайные сообщения пользователю.'''
    sample_responses = ["Потрясающе!", "Я вами горжусь!", "Продолжайте в том же духе!", "Лучшее, что я когда-либо видел!"]
    return random.choice(sample_responses)

if __name__ == '__main__':
    app.run()


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
    button = URLButton(title='Arsenal', url='http://arsenal.com')
    buttons.append(button)
    button = PostbackButton(title='Other', payload='other')
    buttons.append(button)
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
