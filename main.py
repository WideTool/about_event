import telebot
from telebot import types
from config import token, admins
from db import *
import os

bot = telebot.TeleBot(token)

current_event_index = 0
msg_id = None

@bot.message_handler(commands=['start'])
def start_message(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttton_1=types.KeyboardButton(
        text='Расписание'
    )
    # button_2=types.KeyboardButton(
    #     text='Задать вопрос'
    # )
    button_3=types.KeyboardButton(
        text='События'
    )
    
    if message.chat.id in admins:
        button_4=types.KeyboardButton(
            text='Добавить событие'
        )
        button_5=types.KeyboardButton(
            text='Изменить событие'
        )
        button_6=types.KeyboardButton(
            text='Удалить все события'
        )
        markup.add(
            button_4,
            button_5,
            button_6
        )
    
    markup.add(
        buttton_1,
        button_3
    )
    
    bot.send_message(
        message.chat.id, 
        "Привет, это информационный бот конференции - Открытое Сердце. \nСо мной вы можете: \n• Узнать расписание\n• Узнать события сегодняшнего дня",
        reply_markup=markup
    )

@bot.message_handler(content_types=['text'])
def buttons_commands(message):
    if message.text == 'Расписание':
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_1=types.KeyboardButton(
            text='23 февраля'
        )
        button_2=types.KeyboardButton(
            text='24 февраля'
        )
        button_3=types.KeyboardButton(
            text='25 февраля'
        )
        markup.add(
            button_1,
            button_2,
            button_3
        )

        bot.send_message(
            message.chat.id,
            text='На какой день хотите посмотреть расписание?',
            reply_markup=markup
        )
        bot.register_next_step_handler(message, ert)

    # elif message.text == 'Задать вопрос':
    #     bot.send_message(message.chat.id, "Вы можете написать свой вопрос нашим организаторам:")
        
    elif message.text == 'События':
        send_events(message.chat.id)
    
    elif message.text == 'Добавить событие':
        if message.chat.id in admins:
            bot.send_message(message.chat.id, "Введите тему события:")
            bot.register_next_step_handler(message, add_event_theme)

    elif message.text == 'Изменить событие':
        if message.chat.id in admins:
            bot.send_message(message.chat.id, "Введите номер события, которое хотите изменить:")
            bot.register_next_step_handler(message, edit_event)

    elif message.text == 'Удалить все события':
        if message.chat.id in admins:
            clear_events(message)

def ert(message):
    if message.text == "23 февраля":
        msg = bot.send_message(message.chat.id, text = "Пятница:\n14:00 - трапеза\n15:00 - открытие конференции\n16:20 - служение\n18:30 - трапеза\n19:30 - вечер хвалы\n21:00 - расселение")
        bot.pin_chat_message(message.chat.id, msg.id)
        start_message(message)
    elif message.text == "24 февраля":
        msg = bot.send_message(message.chat.id, text = "Суббота:\n09:00 - молитва и прославление\n09:30 - первое служение\n11:20 - общение, игры на знакомства\n13:00 - трапеза\n14:30 - круглые столы\n16:00 - перерыв\n16:30 - второе служение\n19:00 - трапезв\n20:00 - общение, прогулка по городу, волейбол")
        bot.pin_chat_message(message.chat.id, msg.id)
        start_message(message)
    elif message.text == "25 февраля":
        msg = bot.send_message(message.chat.id, text = "Воскресенье:\n10:00 - молитва и прославление\n10:30 - служение, закрытие конференции\n12:00 - свободное время\n13:00 - трапеза\n14:00 - разъезд")
        bot.pin_chat_message(message.chat.id, msg.id)
        start_message(message)
    else:
        pass

def clear_events(message):
    events = Admin.get_events()

    for event in events:
        os.remove(event[2])
        
    Admin.clear_events()

    bot.send_message(message.chat.id, "Все события удалены.")

def add_event_theme(message):
    theme = message.text
    bot.send_message(message.chat.id, "Введите описание события:")
    bot.register_next_step_handler(message, add_event_description, theme)

def add_event_description(message, theme):
    description = message.text
    bot.send_message(message.chat.id, "Отправьте фото события:")
    bot.register_next_step_handler(message, add_event_photo, theme, description)

def add_event_photo(message, theme, description):
    if message.photo:
        photo = message.photo[-1]
        photo_id = photo.file_id
        photo_info = bot.get_file(photo_id)
        downloaded_photo = bot.download_file(photo_info.file_path)
        
        event_number = Admin.get_next_event_number()
        photo_path = f"photo\event_{event_number}.jpg"
        
        with open(photo_path, 'wb') as new_photo:
            new_photo.write(downloaded_photo)
        
        Admin.add_event(theme, description, photo_path, event_number)
        bot.send_message(message.chat.id, "Событие успешно добавлено.")
    else:
        bot.send_message(message.chat.id, "Вы не отправили фото. Попробуйте еще раз.")

def edit_event(message):
    event_number = int(message.text)
    bot.send_message(message.chat.id, "Введите новую тему события:")
    bot.register_next_step_handler(message, edit_event_theme, event_number)

def edit_event_theme(message, event_number):
    theme = message.text
    bot.send_message(message.chat.id, "Введите новое описание события:")
    bot.register_next_step_handler(message, edit_event_description, event_number, theme)

def edit_event_description(message, event_number, theme):
    description = message.text
    bot.send_message(message.chat.id, "Отправьте новое фото события или введите точку что бы оставить нынешнее:")
    bot.register_next_step_handler(message, edit_event_photo, event_number, theme, description)

def edit_event_photo(message, event_number, theme, description):
    if message.photo:
        photo = message.photo[-1]
        photo_id = photo.file_id
        photo_info = bot.get_file(photo_id)
        downloaded_photo = bot.download_file(photo_info.file_path)
        
        os.remove(f"photo\event_{event_number}.jpg")

        photo_path = f"photo\event_{event_number}.jpg"
        
        with open(photo_path, 'wb') as new_photo:
            new_photo.write(downloaded_photo)
    else:
        photo_path = f"photo\event_{event_number}.jpg"
    
    Admin.edit_event_by_number(event_number, theme, description, photo_path)
    bot.send_message(message.chat.id, f"Событие {event_number} успешно изменено.")

def send_events(chat_id, event=None, button=0):
    global current_event_index
    global msg_id

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    events = Admin.get_events()

    if not events:  # Проверяем, есть ли события
        bot.send_message(chat_id, "Нет доступных событий.")
        return

    if event is None:
        if len(events) >= 1:
            keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='previous_event'),
                         types.InlineKeyboardButton(text='Вернуться в меню', callback_data='return_to_menu'))
        else:
            keyboard.add(types.InlineKeyboardButton(text='Вернуться в меню', callback_data='return_to_menu'))

        caption = f"Тема: {events[-1][0]}\nОписание: {events[-1][1]}"  # Последняя запись
        photo_path = events[-1][2]

        with open(photo_path, 'rb') as photo:
            if button == 0:
                msg = bot.send_photo(chat_id, photo, caption=caption, reply_markup=keyboard)
                msg_id = msg.id
            else:
                bot.edit_message_media(types.InputMediaPhoto(photo), chat_id, msg_id, reply_markup=keyboard)
                bot.edit_message_caption(caption, chat_id, msg_id, reply_markup=keyboard)
    else:
        if current_event_index >= 1:
            if current_event_index == len(events) - 1:
                keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='previous_event'),
                             types.InlineKeyboardButton(text='Вернуться в меню', callback_data='return_to_menu'))
            else:
                keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='previous_event'),
                             types.InlineKeyboardButton(text='Вперёд', callback_data='next_event'),
                             types.InlineKeyboardButton(text='Вернуться в меню', callback_data='return_to_menu'))
        elif current_event_index < 1:
            keyboard.add(types.InlineKeyboardButton(text='Вперёд', callback_data='next_event'),
                         types.InlineKeyboardButton(text='Вернуться в меню', callback_data='return_to_menu'))

        ev = event[0]
        caption = f"Тема: {ev[0]}\nОписание: {ev[1]}"
        photo_path = ev[2]

        with open(photo_path, 'rb') as photo:
            bot.edit_message_media(types.InputMediaPhoto(photo), chat_id, msg_id, reply_markup=keyboard)
            bot.edit_message_caption(caption, chat_id, msg_id, reply_markup=keyboard)

def next_event(chat_id):
    global current_event_index
    events = Admin.get_events()

    if current_event_index < len(events) - 1:
        current_event_index += 1
        send_events(chat_id, event=[events[current_event_index]])
    else:
        send_events(chat_id, event=[events[current_event_index]], button=0)

def previous_event(chat_id):
    global current_event_index
    events = Admin.get_events()

    if current_event_index > 0:
        current_event_index -= 1
        send_events(chat_id, event=[events[current_event_index]])
    else:
        send_events(chat_id, event=[events[current_event_index]], button=0)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call: types.CallbackQuery):
    if call.data == 'next_event':
        next_event(call.message.chat.id)
    elif call.data == 'previous_event':
        previous_event(call.message.chat.id)
    elif call.data == 'return_to_menu':
        start_message(call.message)

if __name__ == '__main__':
    try:
        bot.polling()
    except Exception as e:
        print(e)
        bot.polling()
# bot.polling()