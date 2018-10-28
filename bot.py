# -*- coding: utf-8 -*-
import configparser
from telebot import TeleBot, types
from pprint import pprint

config = configparser.ConfigParser()
config.read('config.ini')

token = config['DEFAULT']['BOT_API_TOKEN']
bot = TeleBot(token) 

safe_users = set()

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    msg = """Olá, bem-vindo ao lgbt safe!
    Este grupo foi feito para garantir nossa segurança dentro da universidade."""
    bot.reply_to(message, msg)  

def gen_markup(one_time_keyboard=True, resize_keyboard=True, selective=False):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=one_time_keyboard, 
    resize_keyboard=resize_keyboard, selective=selective)
    markup.add(types.KeyboardButton("Sim!"))
    return markup 

@bot.message_handler(commands=['check'])
def message_handler(message):
    if (len(safe_users) > 0):
        if (message.from_user.id not in safe_users):
            msg = "@{}, você está safe?".format(message.from_user.username) 
            response = bot.send_message(message.chat.id, msg, reply_markup=gen_markup(selective=True))
    else:
        msg = "Você está safe?"
        response = bot.send_message(message.chat.id, msg, reply_markup=gen_markup())
    
    # bot.register_next_step_handler(response, process_response)

@bot.message_handler(commands=['safes'])
def message_handler_safes(message):
    try:  
        users = []
        print(safe_users)
        for user_id in safe_users:  
            #print(user_id, bot.get_chat_member(message.chat.id, user_id))
            users.append(bot.get_chat_member(message.chat.id, user_id).user.first_name)
        bot.reply_to(message, ', '.join(users))  
    except Exception as e:
        bot.reply_to(message, 'ops, ninguém chegou :(')

@bot.message_handler(commands=['clean'])
def message_handler_clean(message):
    safe_users = set()

def process_response(message):
    try:
        chat_id = message.chat.id   
        safe_users.add(chat_id)  
        bot.send_message(chat_id, 'Ufa, ' + message.from_user.first_name)
    except Exception as e:
        bot.reply_to(message, 'oooops')

@bot.message_handler(func=lambda message: message.text == 'Sim!' and message.content_type == 'text')
def message_handler_response(message):
    try:  
        chat_id = message.chat.id  
        user_id = message.from_user.id
        safe_users.add(user_id)  
        bot.send_message(chat_id, 'Ufa, ' + message.from_user.first_name)
    except Exception as e: 
        bot.reply_to(message, 'oooops')

bot.polling(none_stop=True)