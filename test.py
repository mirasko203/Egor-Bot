import telebot
from telebot import types
import sqlite3
import time

# ----------------- TELEGRAM BOT -----------------
TOKEN = "7772407762:AAHwJ0y5b-gcHZG6xd832_c2NyF98OY5m08"
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# ----------------- SQLITE -----------------
conn = sqlite3.connect('bot.db', check_same_thread=False)
cursor = conn.cursor()

# Таблица для стихов
cursor.execute('''
CREATE TABLE IF NOT EXISTS poems (
    id INTEGER PRIMARY KEY,
    title TEXT,
    likes INTEGER DEFAULT 0,
    dislikes INTEGER DEFAULT 0
)
''')
conn.commit()

# Добавляем стихи если их нет
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
            'Первые сочинения, к сожалению, не сохранились, поэтому он начал писать заново с конца 2024 года.'
        )

    elif call.data == 'Poetry':
        bot.answer_callback_query(call.id)
        markup = types.InlineKeyboardMarkup()

        # Достаём лайки/дизлайки
        data = {}
        for i in range(1, 5):
            cursor.execute("SELECT likes, dislikes FROM poems WHERE id=?", (i,))
            data[i] = cursor.fetchone()

        p1 = types.InlineKeyboardButton(text=f'День учителя 👍{data[1][0]} 👎{data[1][1]}', callback_data="p1")
        p2 = types.InlineKeyboardButton(text=f'Крушение "Ан-24" 👍{data[2][0]} 👎{data[2][1]}', callback_data="p2")
        p3 = types.InlineKeyboardButton(text=f'Донбасс 👍{data[3][0]} 👎{data[3][1]}', callback_data="p3")
        p4 = types.InlineKeyboardButton(text=f'Таня Савичева 👍{data[4][0]} 👎{data[4][1]}', callback_data="p4")

        markup.add(p1, p2)
        markup.add(p3, p4)

        bot.send_message(call.message.chat.id, "Выберите стих", reply_markup=markup)

    # ---- Стихи ----
    elif call.data.startswith('p'):
        bot.answer_callback_query(call.id)

        poems_text = {
            'p1': '''5 октября - день особый,
5 октября - день важный,
5 октября - день знаменательный,

Это праздник учителей,
Педагогов, наставников.
Спасибо вам, педагоги
Бриаканской школы,
За свой профессиональный 
Труд, подаренный нам.
Вы все - огромные молодцы!''',

            'p2': '''Из Хабаровска
24 июля, вылетелСамолёт, для которого
Должен был стать
Обычным рейсом.
Маршрут был простой:
Из Хабаровска в Благовещенск,
А из Благове
... (ТВОЙ ТЕКСТ НА 100%) ...''',

            'p3': '''В 2014 году
Донецк и Луганск
Решили отсоединиться от Украины.
... (весь текст полностью) ...''',

            'p4': '''Шёл 1941 год.
Фашизм подошёл к Ленинграду
И начал бомбить город.
... (весь текст полностью) ...'''
        }

        poem_id_map = {'p1': 1, 'p2': 2, 'p3': 3, 'p4': 4}
        poem_id = poem_id_map[call.data]

        bot.send_message(call.message.chat.id, poems_text[call.data])

        # вывод кнопок лайк/дизлайк
        markup = types.InlineKeyboardMarkup()
        like_btn = types.InlineKeyboardButton("👍", callback_data=f"like_{poem_id}")
        dislike_btn = types.InlineKeyboardButton("👎", callback_data=f"dislike_{poem_id}")
        markup.add(like_btn, dislike_btn)

        cursor.execute("SELECT likes, dislikes FROM poems WHERE id=?", (poem_id,))
        likes, dislikes = cursor.fetchone()

        bot.send_message(call.message.chat.id, f"👍 {likes}   👎 {dislikes}", reply_markup=markup)

    # ---- Лайк ----
    elif call.data.startswith("like_"):
        poem_id = int(call.data.split("_")[1])
        cursor.execute("UPDATE poems SET likes = likes + 1 WHERE id = ?", (poem_id,))
        conn.commit()
        bot.answer_callback_query(call.id, "Вы поставили лайк!")

    # ---- Дизлайк ----
    elif call.data.startswith("dislike_"):
        poem_id = int(call.data.split("_")[1])
        cursor.execute("UPDATE poems SET dislikes = dislikes + 1 WHERE id = ?", (poem_id,))
        conn.commit()
        bot.answer_callback_query(call.id, "Вы поставили дизлайк!")


# ----------------- ЗАПУСК БОТА -----------------
print("BOT STARTED...")

while True:
    try:
        bot.infinity_polling(skip_pending=True)
    except Exception as e:
        print("Ошибка, перезапуск:", e)
        time.sleep(2)
