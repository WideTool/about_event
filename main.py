import telebot
from telebot import types

import os

from config import token, admins
from db import User

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start_message(message: types.Message):
    if message.chat.id == User.check_user(message.chat.id):
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttton_1=types.InlineKeyboardButton(
            text='Расписание',
            callback_data="apen"
            )
        button_2=types.InlineKeyboardButton(
            text='Задать вопрос',
            callback_data="help"
            )
        button_3=types.InlineKeyboardButton(
            text='События',
            callback_data="events"
            )
        button_4=types.InlineKeyboardButton(
            text='Добавить событие',
            callback_data="add_event"
            )
        markup.add(
            buttton_1, 
            button_2, 
            button_3
            )
        
        if message.chat.id in admins:
            markup.add(
                button_4
            )
            
        bot.send_message(
            message.chat.id, 
            "Привет, это информационный бот конференции - Открытое Сердце. \nСо мной вы можете: \n• Узнать расписание\n• Узнать события сегодняшнего дня\n• Задать вопрос тех. Поддержке",
            reply_markup=markup
            )
    else:
        bot.send_message(message.chat.id, "Необходимо зарегистрироваться, введите пожалуйста полное имя точно также как и в форме")
        bot.register_next_step_handler(message, registration)

def registration(message):
    User.reg(message.chat.id, message.text)
    bot.send_message(message.chat.id, "Регистрация прошла успешно")
    start_message(message)

@bot.message_handler(commands=['help'])
def help_message(message):
    msg = """
    /start - Главное меню
    /help - Помощь по боту
    """

def set_day(message, day: 0):
    if day == 0:
        markup = types.InlineKeyboardMarkup()
        button_1 = types.InlineKeyboardButton(text='1 день', callback_data='1')
        button_2 = types.InlineKeyboardButton(text='2 день', callback_data='2')
        button_3 = types.InlineKeyboardButton(text='3 день', callback_data='3')
        markup.add(button_1, button_2, button_3)

        bot.send_message(message.chat.id, 'Выберите день', reply_markup=markup)
    
    elif day == 1:
        bot.send_photo(message.chat.id, photo=open(f'{os.path.dirname}\img\one_day.jpg', 'rb'), caption="Лови расписание на первый день")
    elif day == 2:
        bot.send_photo(message.chat.id, photo=open(f'{os.path.dirname}\img\two_day.jpg', 'rb'), caption="Лови расписание на второй день")
    elif day == 3:
        bot.send_photo(message.chat.id, photo=open(f'{os.path.dirname}\img\three_day.jpg', 'rb'), caption="Лови расписание на третий день")

def events(message):
    bot.send_message(message.chat.id, "События")

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Расписание на день
    if call.data == 'apen':
        set_day(call.message)
    elif call.data == '1':
        set_day(call.message, 1)
    elif call.data == '2':
        set_day(call.message, 2)
    elif call.data == '3':
        set_day(call.message, 3)
    
    # События
    elif call.data == 'events':
        events(call.message)

bot.polling()
    
    