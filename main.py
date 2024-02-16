import telebot
from telebot import types
from config import token, admins
import sqlite3
# db = sqlite3.connect('qwe.db', check_same_thread=False)
# cursor = db.cursor()
# cursor.execute("""CREATE TABLE  IF NOT EXISTS users(
#     id TEXT,
#     username TEXT,
#     message TEXT
    
# )""")
# db.commit()

# cursor.execute(f'SELECT qw FROM users WHERE id = "{user_id}" ')
# if cursor.fetchone() is None:
#     cursor.execute(f'INSERT INTO users VALUES(?, ?, ?)', (user_id, username, user_message))
#     db.commit()
# else:
#     for value in cursor.execute("SELECT * FROM users"):
#         print(value)
bot = telebot.TeleBot(token)
@bot.message_handler(commands=['start'])
def start_message(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttton_1=types.KeyboardButton(
        text='расписание'
        )
    button_2=types.KeyboardButton(
        text='задать вопрос'
        )
    button_3=types.KeyboardButton(
        text='события'
        )
    if message.id in admins:
        markup.add(
            button_4,
            button_5,
            button_6
        )
    button_4=types.KeyboardButton(
        text='добавить событие'
        )
    button_5=types.KeyboardButton(
        text='изменить(что то)'
    )
    button_6=types.KeyboardButton(
        text='данные пользователей'
        )
    markup.add(
        buttton_1, 
        button_2, 
        button_3
        )
    bot.send_message(
        message.chat.id, 
        "привет, это информационнаый бот. С моими возможностями,"
        "вы можете ознакомиться введя команду /help",
        reply_markup=markup
        )
@bot.message_handler(content_types=['text'])
def buttons_commands(message):
    if message.text == 'расписание':
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_1=types.KeyboardButton(
            text='20 января'
            )
        button_2=types.KeyboardButton(
            text='21 января'
            )
        button_3=types.KeyboardButton(
            text='23 января'
            )
        markup.add(
            button_1,
            button_2,
            button_3
        )
        bot.send_message(
            message.chat.id,
            text='на кокой день хотите посмотреть расписание?',
            reply_markup=markup
            )
        
bot.polling()
    
    