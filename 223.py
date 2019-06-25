import os
import sys
from time import sleep
from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

led_status = '0'

channel_secret = 'cbb9d3666ab6ef97566553fa8d7d19d9'
channel_access_token = '4mAQi/u/9682zF5OwqporCSEirpe+7/8jb33Ze8bMkbrqqEbfXpAA4Mh2kjdBe6u8zUPijR1A+dX8qoL6YPnSFaK28a+sts5qsyKmtu2p/YydaOO+UVd8QtXImSc+7KVAUGEmsoxDxQmF3AcUcyLzgdB04t89/1O/w1cDnyilFU='

if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@app.route("/")
def control_led():
    global led_status
    return led_status

@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    global led_status
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )
    print event.message.text

    #in_w = event.message.text[0]
    in_w = ""
    
    for text in event.message.text :
        in_w = in_w + text
    

    if ('客廳開燈' == in_w.encode('utf-8')):
        led_status = '00'
        sleep ( 2 )
        led_status = '1'
    elif('客廳關燈' == in_w.encode('utf-8')):
        led_status = '0'
        sleep ( 2 )
        led_status = '1'
    elif('插座關' == in_w.encode('utf-8')):
        led_status = '2'
        sleep ( 2 )
        led_status = '1'
    elif('插座開' == in_w.encode('utf-8')):
        led_status = '22'
        sleep ( 2 )
        led_status = '1'
    elif('房間開燈' == in_w.encode('utf-8')):
        led_status = '33'
        sleep ( 2 )
        led_status = '5'
    elif('房間關燈' == in_w.encode('utf-8')):
        led_status = '3'
        sleep ( 2 )
        led_status = '5'
	

    print "led:" + led_status

if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000,help='port')
    arg_parser.add_argument('-d', '--debug', default=True, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port, host='0.0.0.0')
