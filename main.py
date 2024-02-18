import telebot
from telebot import types
from config import token, admins
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
    if message.chat.id in admins:
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
            button_4,
            button_5,
            button_6
        )
    
    markup.add(
        buttton_1, 
        button_2, 
        button_3
        )
    bot.send_message(
        message.chat.id, 
        "привет, это информационный бот. С моими возможностями,"
        "вы можете ознакомиться введя команду /help",
        reply_markup=markup
        )

@bot.message_handler(content_types=['text'])
def buttons_commands(message):
    if message.text == 'расписание':
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
            text='на какой день хотите посмотреть расписание?',
            reply_markup=markup
            )
        bot.register_next_step_handler(message, ert)
def ert(message):
    if message.text == "23 февраля":
        bot.send_message(message.chat.id, text = "Пятница:\n14:00 - трапеза\n15:00 - открытие конференции\n16:20 - служение\n18:30 - трапеза\n19:30 - вечер хвалы\n21:00 - расселение")
    elif message.text == "24 февраля":
        bot.send_message(message.chat.id, text = "Суббота:\n09:00 - молитва и прославление\n09:30 - первое служение\n11:20 - общение, игры на знакомства\n13:00 - трапеза\n14:30 - круглые столы\n16:00 - перерыв\n16:30 - второе служение\n19:00 - трапезв\n20:00 - общение, прогулка по городу, волейбол")
    elif message.text == "25 февраля":
        bot.send_message(message.chat.id, text = "Воскресенье:\n10:00 - молитва и прославление\n10:30 - служение, закрытие конференции\n12:00 - свободное время\n13:00 - трапеза\n14:00 - разъезд")
    else:
        bot.send_message(message.chat.id, text ="")
bot.polling()