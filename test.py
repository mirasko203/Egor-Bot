import telebot              # Для работы с Telegram
from telebot import types   # Для inline-кнопок
import sqlite3              # Для хранения лайков/дизлайков

# ----------------- TELEGRAM BOT -----------------
TOKEN = '7772407762:AAHwJ0y5b-gcHZG6xd832_c2NyF98OY5m08'
bot = telebot.TeleBot(TOKEN)

# ----------------- SQLITE -----------------
conn = sqlite3.connect('bot.db', check_same_thread=False)
cursor = conn.cursor()

# Создаём таблицу стихов, если её нет
cursor.execute('''
CREATE TABLE IF NOT EXISTS poems (
    id INTEGER PRIMARY KEY,
    title TEXT,
    likes INTEGER DEFAULT 0,
    dislikes INTEGER DEFAULT 0
)
''')
conn.commit()

# Добавляем стихи, если их нет
poems = [
    (1, 'День учителя'),
    (2, 'Крушение "Ан-24"'),
    (3, 'Донбасс'),
    (4, 'Таня Савичева')
]
for poem_id, title in poems:
    cursor.execute('INSERT OR IGNORE INTO poems (id, title) VALUES (?, ?)', (poem_id, title))
conn.commit()

# ----------------- /start -----------------
@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Об авторе💭', callback_data="Autor")
    btn2 = types.InlineKeyboardButton(text='Стихи автора📜', callback_data="Poetry")
    keyboard.add(btn1, btn2)
    bot.send_message(message.chat.id, 
                     'Это бот Шульмина Егора. Тут будут его произведения и краткая история жизни', 
                     reply_markup=keyboard)

# ----------------- CALLBACK -----------------
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == 'Autor':
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id,
                         'Шульми́н Егор Александрович родился 25 июля 2013 года в городе Хабаровск. '
                         'На данный момент живёт в селе Бриакан, р-на им. Полины Осипенко. '
                         'С ранних лет Егор умеет читать. Писать стихи начал в 9 лет. '
                         'Первые сочинения, к сожалению, не сохранились, поэтому он начал писать заново с конца 2024 года.')
    elif call.data == 'Poetry':
        bot.answer_callback_query(call.id)
        markup = types.InlineKeyboardMarkup()
        # Получаем количество лайков/дизлайков
        cursor.execute("SELECT likes, dislikes FROM poems WHERE id = 1")
        l1,d1 = cursor.fetchone()
        cursor.execute("SELECT likes, dislikes FROM poems WHERE id = 2")
        l2,d2 = cursor.fetchone()
        cursor.execute("SELECT likes, dislikes FROM poems WHERE id = 3")
        l3,d3 = cursor.fetchone()
        cursor.execute("SELECT likes, dislikes FROM poems WHERE id = 4")
        l4,d4 = cursor.fetchone()
        # Создаём кнопки с количеством лайков/дизлайков
        p1 = types.InlineKeyboardButton(text=f'День учителя 👍{l1} 👎{d1}', callback_data="p1")
        p2 = types.InlineKeyboardButton(text=f'Крушение "Ан-24" 👍{l2} 👎{d2}', callback_data='p2')
        p3 = types.InlineKeyboardButton(text=f'Донбасс 👍{l3} 👎{d3}', callback_data='p3')
        p4 = types.InlineKeyboardButton(text=f'Таня Савичева 👍{l4} 👎{d4}', callback_data='p4')
        markup.add(p1,p2)
        markup.add(p3,p4)
        bot.send_message(call.message.chat.id, "Выберите стих", reply_markup=markup)
    elif call.data.startswith('p'):
        bot.answer_callback_query(call.id)
        poems_text = {
            'p1':'5 октября - день особый,\n5 октября - день важный,\n5 октября - день знаменательный,\n\nЭто праздник учителей,\nПедагогов, наставников.\nСпасибо вам, педагоги\nБриаканской школы,\nЗа свой профессиональный \nТруд, подаренный нам.\nВы все - огромные молодцы!',
            'p2':'Из Хабаровска\n24 июля, вылетелСамолёт, для которого\nДолжен был стать\nОбычным рейсом.\nМаршрут был простой:\nИз Хабаровска в Благовещенск,\nА из Благовещенска самолёт \nДолжен был долететь до Тынды.\nНо ещё до взлёта \nБыли проблемы с самолётом.\nЛётчики подумали, "пустяки",\nНо этот пустяк стал роковым.\n1 круг. Нормально.\n2 круг. Упал.\nЛишь спустя часы\nНашли, к сожалению\nОбломки самолёта.\nНикто не выжил...',
            'p3':'В 2014 году\nДонецк и Луганск\nРешили отсоединиться от Украины.\nС тех пор, 8 лет\nДонбасс подвергался бомбардировки,\nУнижению и заставлению\nОбратно вернуться в Украину.\nНо 24 февраля 22 года\nНаши войска пришли\nСпасать население от "новоцистов¹".\nПровели народное голосование,\nИ практически все \nБыли согласны.\nИ вот настал момент:\n30 сентября 2022 года\nДонецк, Луганск, Херсон, Запорожье - \nЭто новый, русский Донбасс.\nСегодня, 1 октября 2025 года\nДонбасс празднует\nВоссоединение с Россией.',
            'p4':'Шёл 1941 год.\nФашизм подошёл к Ленинграду\nИ начал бомбить город.\nТаня, видя это всё,\nЗаводит личный дневник.\nЕё первая запись была такова:\n"Женя умерла 28 дек в 12:00 часа утра 1941 г.".\nИ так, с каждым родственником\nПонемногу Таня\nСтановилась сиротой.\nПозже она потеряла почти всех\nСвоих родственников.\nНикого у неё не осталось.\nСловно она жила на\nНеобитаемом острове.\nНо 1 июля Таня умерла.\nОт серьезной болезни.\nБлагодаря старшим сестре\nНине и брату Михаилу\nМы можем прочесть о\nТом, как было тяжело Тане.'
        }
        poem_id_map = {'p1':1,'p2':2,'p3':3,'p4':4}
        poem_id = poem_id_map[call.data]
        bot.send_message(call.message.chat.id, poems_text[call.data])
        # Кнопки лайк/дизлайк
        markup = types.InlineKeyboardMarkup()
        like_btn = types.InlineKeyboardButton("👍", callback_data=f"like_{poem_id}")
        dislike_btn = types.InlineKeyboardButton("👎", callback_data=f"dislike_{poem_id}")
        markup.add(like_btn, dislike_btn)
        # Показываем текущее количество лайков/дизлайков
        cursor.execute("SELECT likes, dislikes FROM poems WHERE id = ?", (poem_id,))
        likes, dislikes = cursor.fetchone()
        bot.send_message(call.message.chat.id, f"👍 {likes}   👎 {dislikes}", reply_markup=markup)
    elif call.data.startswith("like_"):
        poem_id = int(call.data.split("_")[1])
        cursor.execute("UPDATE poems SET likes = likes + 1 WHERE id = ?", (poem_id,))
        conn.commit()
        bot.answer_callback_query(call.id, "Вы поставили лайк!")
        cursor.execute("SELECT likes, dislikes FROM poems WHERE id = ?", (poem_id,))
        likes, dislikes = cursor.fetchone()
        bot.send_message(call.message.chat.id, f"👍 {likes}   👎 {dislikes}")
    elif call.data.startswith("dislike_"):
        poem_id = int(call.data.split("_")[1])
        cursor.execute("UPDATE poems SET dislikes = dislikes + 1 WHERE id = ?", (poem_id,))
        conn.commit()
        bot.answer_callback_query(call.id, "Вы поставили дизлайк!")
        cursor.execute("SELECT likes, dislikes FROM poems WHERE id = ?", (poem_id,))
        likes, dislikes = cursor.fetchone()
        bot.send_message(call.message.chat.id, f"👍 {likes}   👎 {dislikes}")

# ----------------- ЗАПУСК БОТА -----------------
print("BOT STARTED...")
bot.infinity_polling(skip_pending=True)  # Работаем бесконечно
