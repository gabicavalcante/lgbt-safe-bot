# -*- coding: utf-8 -*-
import configparser
from telebot import TeleBot, types

config = configparser.ConfigParser()
config.read('config.ini')

token = config['DEFAULT']['BOT_API_TOKEN']
bot = TeleBot(token) 

safe_users = []

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    msg = """Olá, bem-vindo ao lgbt safe!
    Este grupo foi feito para garantir nossa segurança dentro da universidade."""
    bot.reply_to(message, msg)  

def gen_markup(one_time_keyboard=True, resize_keyboard=True, selective=False):
    markup = types.ForceReply(one_time_keyboard=one_time_keyboard, 
    resize_keyboard=resize_keyboard, selective=selective)
    markup.add(types.KeyboardButton("Sim!"))
    return markup 

@bot.message_handler(commands=['check'])
def message_handler(message):
    if (len(safe_users) > 0):
        if (message.from_user.username not in safe_users):
            msg = "@{}, você está safe?".format(message.from_user.username) 
            response = bot.send_message(message.chat.id, msg, reply_markup=gen_markup(selective=True))
    else:
        msg = "Você está safe?"
        response = bot.send_message(message.chat.id, msg, reply_markup=gen_markup())
    
    bot.register_next_step_handler(response, process_response)

@bot.message_handler(commands=['safes'])
def message_handler_safes(message):
    try:
        bot.reply_to(message, ', '.join(safe_users))  
    except Exception as e:
        bot.reply_to(message, 'ops, ninguém chegou :(')

@bot.message_handler(commands=['clean'])
def message_handler_clean(message):
    safe_users = []

def process_response(message):
    try:
        chat_id = message.chat.id   
        safe_users.append(message.from_user.username)  
        bot.send_message(chat_id, 'Ufa, ' + message.from_user.username)
    except Exception as e:
        bot.reply_to(message, 'oooops')
     
bot.polling(none_stop=True)