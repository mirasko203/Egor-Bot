import telebot
from telebot import types

TOKEN = '7772407762:AAHwJ0y5b-gcHZG6xd832_c2NyF98OY5m08'
bot = telebot.telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])

def start(message):
	keyboard = types.InlineKeyboardMarkup()

	btn1 = types.InlineKeyboardButton(text='Об авторе💭', callback_data="Autor")
	btn2 = types.InlineKeyboardButton(text='Стихи автора📜', callback_data=('Poetry'))

	keyboard.add(btn1)
	keyboard.add(btn2)

	bot.send_message(message.chat.id, 'Это бот Шульмина Егора. Тут будут его произведения и краткая история жизни', reply_markup=keyboard)

@bot.callback_query_handler(func = lambda call: True)
def callback(call):
	if call.data == 'Autor':
		bot.answer_callback_query(call.id)
		bot.send_message(call.message.chat.id, 'Шульми́н Егор Александрович родился 25 июля 2013 года в городе Хабаровск. На данный момент живёт в селе Бриакан, р-на им. Полины Осипенко. С ранних лет Егор умеет читать. Писать стихи начал в 9 лет. Первые сочинения, к сожалению, не сохранились, поэтому он начал писать заново с конца 2024 года.')

	elif call.data == 'Poetry':
		bot.answer_callback_query(call.id)

		markup = types.InlineKeyboardMarkup()

		p1 = types.InlineKeyboardButton(text='День учителя', callback_data="p1")
		p2 = types.InlineKeyboardButton(text='Крушение "Ан-24"', callback_data='p2')
		p3 = types.InlineKeyboardButton(text='Донбасс', callback_data='p3')
		p4 = types.InlineKeyboardButton(text="Таня Савичева", callback_data='p4')

		markup.add(p1)
		markup.add(p2)
		markup.add(p3)
		markup.add(p4)

		bot.send_message(call.message.chat.id, "Выберите стих", reply_markup=markup)

	elif call.data == 'p1':
		bot.answer_callback_query(call.id)
		bot.send_message(call.message.chat.id, '5 октября - день особый,\n5 октября - день важный,\n5 октября - день знаменательный,\n\nЭто праздник учителей,\nПедагогов, наставников.\nСпасибо вам, педагоги\nБриаканской школы,\nЗа свой профессиональный \nТруд, подаренный нам.\nВы все - огромные молодцы!')
		markup = types.InlineKeyboardMarkup()

		p1 = types.InlineKeyboardButton(text='День учителя', callback_data="p1")
		p2 = types.InlineKeyboardButton(text='Крушение "Ан-24"', callback_data='p2')
		p3 = types.InlineKeyboardButton(text='Донбасс', callback_data='p3')
		p4 = types.InlineKeyboardButton(text="Таня Савичева", callback_data='p4')

		markup.add(p1)
		markup.add(p2)
		markup.add(p3)
		markup.add(p4)

		bot.send_message(call.message.chat.id, "Выберите стих", reply_markup=markup)

	elif call.data == 'p2':
		bot.answer_callback_query(call.id)
		bot.send_message(call.message.chat.id, 'Из Хабаровска\n24 июля, вылетелСамолёт, для которого\nДолжен был стать\nОбычным рейсом.\nМаршрут был простой:\nИз Хабаровска в Благовещенск,\nА из Благовещенска самолёт \nДолжен был долететь до Тынды.\nНо ещё до взлёта \nБыли проблемы с самолётом.\nЛётчики подумали, "пустяки",\nНо этот пустяк стал роковым.\n1 круг. Нормально.\n2 круг. Упал.\nЛишь спустя часы\nНашли, к сожалению\nОбломки самолёта.\nНикто не выжил...')
		markup = types.InlineKeyboardMarkup()

		p1 = types.InlineKeyboardButton(text='День учителя', callback_data="p1")
		p2 = types.InlineKeyboardButton(text='Крушение "Ан-24"', callback_data='p2')
		p3 = types.InlineKeyboardButton(text='Донбасс', callback_data='p3')
		p4 = types.InlineKeyboardButton(text="Таня Савичева", callback_data='p4')

		markup.add(p1)
		markup.add(p2)
		markup.add(p3)
		markup.add(p4)

		bot.send_message(call.message.chat.id, "Выберите стих", reply_markup=markup)


	elif call.data == 'p3':
		bot.answer_callback_query(call.id)
		bot.send_message(call.message.chat.id, 'В 2014 году\nДонецк и Луганск\nРешили отсоединиться от Украины.\nС тех пор, 8 лет\nДонбасс подвергался бомбардировки,\nУнижению и заставлению\nОбратно вернуться в Украину.\nНо 24 февраля 22 года\nНаши войска пришли\nСпасать население от "новоцистов¹".\nПровели народное голосование,\nИ практически все \nБыли согласны.\nИ вот настал момент:\n30 сентября 2022 года\nДонецк, Луганск, Херсон, Запорожье - \nЭто новый, русский Донбасс.\nСегодня, 1 октября 2025 года\nДонбасс празднует\nВоссоединение с Россией.\n')
		markup = types.InlineKeyboardMarkup()

		p1 = types.InlineKeyboardButton(text='День учителя', callback_data="p1")
		p2 = types.InlineKeyboardButton(text='Крушение "Ан-24"', callback_data='p2')
		p3 = types.InlineKeyboardButton(text='Донбасс', callback_data='p3')
		p4 = types.InlineKeyboardButton(text="Таня Савичева", callback_data='p4')

		markup.add(p1)
		markup.add(p2)
		markup.add(p3)
		markup.add(p4)

		bot.send_message(call.message.chat.id, "Выберите стих", reply_markup=markup)


	elif call.data == 'p4':
		bot.answer_callback_query(call.id)
		bot.send_message(call.message.chat.id, 'Шёл 1941 год.\nФашизм подошёл к Ленинграду\nИ начал бомбить город.\nТаня, видя это всё,\nЗаводит личный дневник.\nЕё первая запись была такова:\n"Женя умерла 28 дек в 12:00 часа утра 1941 г.".\nИ так, с каждым родственником\nПонемногу Таня\nСтановилась сиротой.\nПозже она потеряла почти всех\nСвоих родственников.\nНикого у неё не осталось.\nСловно она жила на\nНеобитаемом острове.\nНо 1 июля Таня умерла.\nОт серьезной болезни.\nБлагодаря старшим сестре\nНине и брату Михаилу\nМы можем прочесть о\nТом, как было тяжело Тане.\n')
		markup = types.InlineKeyboardMarkup()

		p1 = types.InlineKeyboardButton(text='День учителя', callback_data="p1")
		p2 = types.InlineKeyboardButton(text='Крушение "Ан-24"', callback_data='p2')
		p3 = types.InlineKeyboardButton(text='Донбасс', callback_data='p3')
		p4 = types.InlineKeyboardButton(text="Таня Савичева", callback_data='p4')

		markup.add(p1)
		markup.add(p2)
		markup.add(p3)
		markup.add(p4)

		bot.send_message(call.message.chat.id, "Выберите стих", reply_markup=markup)





bot.polling(none_stop=True)

import os
from flask import Flask
import threading

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is alive!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_flask, daemon=True).start()

print(f"Flask running on port {port}")
