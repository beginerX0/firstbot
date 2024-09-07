##t.me/SNtstbot



import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot(token)
#вопросы
questions = {'name':'Введите ваше имя: ',
              'age':'Введите ваш возраст: ',
              'department':'На каком факультете вы учитесь?: ',
              'SoS':'Расскажите немного о себе: ',
              'photo': 'Загрузите фотографию'}
#возможность пропуска вопроса
propusk = [False,False,False,True,True]
#словарь который отправится в бд
setup_data=dict()
f=False#нужная для opr штука

qamount = len(questions)
cquestion = 0
def opr(message):
    global propusk
    global cquestion
    global setup_data
    global f
    f = False
    if((cquestion>0)and(cquestion<=qamount)):
        if(propusk[cquestion-1]):
            markup=InlineKeyboardMarkup()
            markup.row_width = 1
            markup.add(InlineKeyboardButton("Пропустить", callback_data="skip"))
            bot.send_message(message.chat.id,questions.get(list(questions.keys())[cquestion-1]),reply_markup=markup)
            @bot.callback_query_handler(func=lambda call: True)
            def callback(call):
                global cquestion
                global setup_data
                global f
                if call.data=='skip':
                    bot.answer_callback_query(call.id, "Пропуск")
                    setup_data.update({list(questions.keys())[cquestion-2]:'none'})
                    if(cquestion<=len(questions)):
                        if(propusk[cquestion-1]):bot.send_message(message.chat.id,questions.get(list(questions.keys())[cquestion-1]),reply_markup=markup)
                        else:bot.send_message(message.chat.id,questions.get(list(questions.keys())[cquestion-1]))
                    else:
                        cquestion=0
                        setup_data.update({'tgid':message.from_user.id,
                           'firstname':message.from_user.first_name,
                           'lastname':message.from_user.last_name})
                        print(setup_data)##вместо вывода в оболочку должен быть метод переноса в БД
                        bot.send_message(message.chat.id,"Спасибо! Ваша анкета сохранена")
                        setup_data=dict()
                    f = True
                    cquestion+=1
        else:bot.send_message(message.chat.id,questions.get(list(questions.keys())[cquestion-1]))
        if(cquestion!=1)and(not f):setup_data.update({list(questions.keys())[cquestion-2]:message.text})
        bot.register_next_step_handler(message,opr)
        cquestion+=1
    elif(cquestion==qamount+1):
        setup_data.update({list(questions.keys())[cquestion-2]:message.text})
        setup_data.update({'tgid':message.from_user.id,
                           'firstname':message.from_user.first_name,
                           'lastname':message.from_user.last_name})
        cquestion=0
        print(setup_data)##вместо вывода в оболочку должен быть метод переноса в БД
        bot.send_message(message.chat.id,"Спасибо! Ваша анкета сохранена")
        setup_data=dict()

@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(message.chat.id,
"""Добро пожаловать! Используйте команду
/setup для настройки вашей анкеты.""")

@bot.message_handler(commands=["setup"])
def setup(message):
    global setup_data
    global cquestion
    def prt(m):print(m.text)
    if(cquestion==0):
        cquestion+=1
        setup_data=dict()
        bot.send_message(message.chat.id,"Здраствуйте")
        opr(message)

bot.infinity_polling()
