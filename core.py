#!/usr/bin/env python
import os
import telegram
import time
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import ImageFormatter
from pygments.styles import get_all_styles

bot = telegram.Bot('XXX')
print list(get_all_styles())
style = 'monokai'
font = 'consolas'

example = '''
from time import localtime

activities = {8: 'Sleeping',
              9: 'Commuting',
              17: 'Working',
              18: 'Commuting',
              20: 'Eating',
              22: 'Resting' }

time_now = localtime()
hour = time_now.tm_hour

for activity_time in sorted(activities.keys()):
    if hour < activity_time:
        print activities[activity_time]
        break
else:
    print 'Unknown, AFK or sleeping!'
'''

shortexample = '''
print 'Hello World'
'''

welcome = '''
Do you want to send your mate a short script? This bot convert your send python source code into beautiful rendered code samples wich are nice to send to your friend. Just send your code to me and I will response with a png that you can pass on to your mate.
/example - Sends you a example code
/settings - Let you setup many different styles etc.
/help - Shows this message
'''

try:
    LAST_UPDATE_ID = bot.getUpdates()[-1].update_id
except IndexError:
    LAST_UPDATE_ID = None

def keyboard(status, chat_id):
    global font
    if status == 1: #Settings
        custom_keyboard  = [
        [ 'Change style' ],
        [ 'Change font' ],
        [ 'Donate' ],
        [ 'Exit', 'Next' ],
        ]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.sendMessage(chat_id=chat_id, text="Choose.", reply_markup=reply_markup)
        pass
    if status == 2: #Styles page 1
        custom_keyboard  = [
        [ 'Monokai' ],
        [ 'Autumn' ],
        [ 'Colorful' ],
        [ 'Back', 'Exit', 'Next' ],
        ]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.sendMessage(chat_id=chat_id, text="Choose.", reply_markup=reply_markup)
        pass
    if status == 3: #Fonts page 1
        custom_keyboard  = [
        [ 'Consolas' ],
        [ 'Impact' ],
        [ 'Comic Sans MS' ],
        [ 'Back', 'Exit', 'Next' ],
        ]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.sendMessage(chat_id=chat_id, text="Choose.", reply_markup=reply_markup)
        pass
    if status > 3: #Close
        reply_markup = telegram.ReplyKeyboardHide()
        bot.sendMessage(chat_id=chat_id, text="Keyboard deactivated", reply_markup=reply_markup)
        pass
    pass

def send(codee, fullpath, chat_id):
    token = highlight(codee, PythonLexer(), ImageFormatter(style=style, font_name=font, line_pad='6', line_number_bg='#272822', line_number_separator=False), format(fullpath.decode().encode('utf-8')))
    bot.sendPhoto(chat_id=chat_id, photo=open(fullpath.decode().encode('utf-8'), 'rb'))
    pass

def echo():
    global LAST_UPDATE_ID
    global style
    global font

    for update in bot.getUpdates(offset=LAST_UPDATE_ID):
        if LAST_UPDATE_ID < update.update_id:
            chat_id = update.message.chat_id
            message = update.message.text.encode('utf-8')
            is_group = update.message.chat_id != update.message.from_user.id
            try:
                username = update.message.from_user.username.decode().encode('utf-8')
                pass
            except:
                try:
                    username = update.message.from_user.first_name.decode().encode('utf-8')
                    pass
                except:
                    username = 'Exeption'
                    pass
                pass
            directory = 'Archiv/' + username
            output = str(LAST_UPDATE_ID) + '.png'
            if not os.path.exists(directory):
                os.makedirs(directory)
            fullpath = directory + '/' + output
            if (is_group == False):
                if message == '/settings':
                    keyboard(1, chat_id)
                    pass
                elif message == '/start':
                    bot.sendMessage(chat_id=chat_id, text='Youre welcome! Just try it to send me a python script!')
                    pass
                elif message == '/example':
                    send(example, fullpath, chat_id)
                    pass
                elif message == '/help':
                    bot.sendMessage(chat_id=chat_id, text='Youre welcome! Just try it to send me a python script!\n/example - Sends you a example code\n/settings - Let you setup many different styles etc.\n/help - Shows this message')
                    pass
                elif message == 'Change style':
                    keyboard(2, chat_id)
                    pass
                elif message == 'Monokai':
                    style = 'monokai'
                    bot.sendMessage(chat_id=chat_id, text='Changed to style: ' + style)
                    send(example, fullpath, chat_id)
                    pass
                elif message == 'Autumn':
                    style = 'autumn'
                    print style
                    bot.sendMessage(chat_id=chat_id, text='Changed to style: ' + style)
                    send(example, fullpath, chat_id)
                    pass
                elif message == 'Colorful':
                    style = 'colorful'
                    bot.sendMessage(chat_id=chat_id, text='Changed to style: ' + style)
                    send(example, fullpath, chat_id)
                    pass
                elif message == 'Change font':
                    keyboard(3, chat_id)
                    pass
                elif message == 'Consolas':
                    font = 'Consolas'
                    send(shortexample, fullpath, chat_id)
                    pass
                elif message == 'Impact':
                    font = 'Impact'
                    send(shortexample, fullpath, chat_id)
                    pass
                elif message == 'Comic Sans MS':
                    font = 'Comic Sans MS'
                    send(shortexample, fullpath, chat_id)
                    pass
                elif message == 'Next':
                    bot.sendMessage(chat_id=chat_id, text='Not yet.')
                    pass
                elif message == 'Back':
                    keyboard(1, chat_id)
                    pass
                elif message == 'Donate':
                    bot.sendMessage(chat_id=chat_id, text='Thank you for supporting this tool. Feel free to send some BTC to this address:\n1NVZ5dX9Ekh14cDHRKTjxYqAcHRJpdYyfN')
                    pass
                elif message == 'Exit':
                    keyboard(99, chat_id)
                    pass
                else:
                    send(message, fullpath, chat_id)
                    pass
                pass
            else:
                if message.startswith("/code "):
                    send(message[6:], fullpath, chat_id)
                    pass
                pass

            LAST_UPDATE_ID = update.update_id


if __name__ == '__main__':
    while True:
        try:
            echo()
            pass
        except:
            print "No connection."
            pass
        time.sleep(1)
