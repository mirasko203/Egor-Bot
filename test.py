import telebot
from telebot import types
import threading
from flask import Flask
import os
import sqlite3

# ================= TELEGRAM BOT =================
TOKEN = "7772407762:AAHwJ0y5b-gcHZG6xd832_c2NyF98OY5m08"
bot = telebot.TeleBot(TOKEN, threaded=False)   # <==== важно, иначе Render ломает polling

# ================= SQLITE =================
conn = sqlite3.connect("bot.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS poems (
    id INTEGER PRIMARY KEY,
    title TEXT,
    likes INTEGER DEFAULT 0,
    dislikes INTEGER DEFAULT 0
)
""")
conn.commit()

poems = [
    (1, 'День учителя'),
    (2, 'Крушение "Ан-24"'),
    (3, 'Донбасс'),
    (4, 'Таня Савичева')
]
for pid, title in poems:
    cursor.execute("INSERT OR IGNORE INTO poems (id, title) VALUES (?, ?)", (pid, title))
conn.commit()


# ================= COMMAND /start =================
@bot.message_handler(commands=['start'])
def start(message):
    kb = types.InlineKeyboardMarkup()
    kb.add(
        types.InlineKeyboardButton("Об авторе💭", callback_data="Autor"),
        types.InlineKeyboardButton("Стихи автора📜", callback_data="Poetry")
    )
    bot.send_message(
        message.chat.id,
        "Это бот Шульмина Егора. Тут будут его произведения и краткая история жизни",
        reply_markup=kb
    )


# ================= CALLBACKS =================
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    cursor = conn.cursor()  # новый курсор для каждого колбэка

    if call.data == "Autor":
        bot.answer_callback_query(call.id)
        bot.send_message(
            call.message.chat.id,
            "Шульми́н Егор Александрович родился 25 июля 2013 года в городе Хабаровск. "
            "На данный момент живёт в селе Бриакан, р-на им. Полины Осипенко. "
            "С ранних лет Егор умеет читать. Писать стихи начал в 9 лет. "
            "Первые сочинения, к сожалению, не сохранились, поэтому он начал писать заново с конца 2024 года."
        )

    elif call.data == "Poetry":
        bot.answer_callback_query(call.id)

        def get_counts(id):
            cursor.execute("SELECT likes, dislikes FROM poems WHERE id=?", (id,))
            return cursor.fetchone()

        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton(f"День учителя 👍{get_counts(1)[0]} 👎{get_counts(1)[1]}", callback_data="p1"),
            types.InlineKeyboardButton(f"Крушение \"Ан-24\" 👍{get_counts(2)[0]} 👎{get_counts(2)[1]}", callback_data="p2"),
        )
        markup.add(
            types.InlineKeyboardButton(f"Донбасс 👍{get_counts(3)[0]} 👎{get_counts(3)[1]}", callback_data="p3"),
            types.InlineKeyboardButton(f"Таня Савичева 👍{get_counts(4)[0]} 👎{get_counts(4)[1]}", callback_data="p4"),
        )

        bot.send_message(call.message.chat.id, "Выберите стих", reply_markup=markup)

    # ---------- выбор стихотворения ----------
    elif call.data.startswith("p"):
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
24 июля, вылетел
Самолёт, для которого
Должен был стать
Обычным рейсом.
Маршрут был простой:
Из Хабаровска в Благовещенск,
А из Благовещенска самолёт 
Должен был долететь до Тынды.
Но ещё до взлёта 
Были проблемы с самолётом.
Лётчики подумали, "пустяки",
Но этот пустяк стал роковым.
1 круг. Нормально.
2 круг. Упал.
Лишь спустя часы
Нашли, к сожалению
Обломки самолёта.
Никто не выжил...''',

            'p3': '''В 2014 году
Донецк и Луганск
Решили отсоединиться от Украины.
С тех пор, 8 лет
Донбасс подвергался бомбардировки,
Унижению и заставлению
Обратно вернуться в Украину.
Но 24 февраля 22 года
Наши войска пришли
Спасать население от "новоцистов¹".
Провели народное голосование,
И практически все 
Были согласны.
И вот настал момент:
30 сентября 2022 года
Донецк, Луганск, Херсон, Запорожье - 
Это новый, русский Донбасс.
Сегодня, 1 октября 2025 года
Донбасс празднует
Воссоединение с Россией.''',

            'p4': '''Шёл 1941 год.
Фашизм подошёл к Ленинграду
И начал бомбить город.
Таня, видя это всё,
Заводит личный дневник.
Её первая запись была такова:
"Женя умерла 28 дек в 12:00 часа утра 1941 г.".
И так, с каждым родственником
Понемногу Таня
Становилась сиротой.
Позже она потеряла почти всех
Своих родственников.
Никого у неё не осталось.
Словно она жила на
Необитаемом острове.
Но 1 июля Таня умерла.
От серьезной болезни.
Благодаря старшим сестре
Нине и брату Михаилу
Мы можем прочесть о
Том, как было тяжело Тане.''',
        }

        poem_id = int(call.data[1])
        bot.send_message(call.message.chat.id, poems_text[call.data])

        cursor.execute("SELECT likes, dislikes FROM poems WHERE id=?", (poem_id,))
        likes, dislikes = cursor.fetchone()

        kb = types.InlineKeyboardMarkup()
        kb.add(
            types.InlineKeyboardButton("👍", callback_data=f"like_{poem_id}"),
            types.InlineKeyboardButton("👎", callback_data=f"dislike_{poem_id}")
        )

        bot.send_message(call.message.chat.id, f"👍 {likes}   👎 {dislikes}", reply_markup=kb)

    # ---------- ЛАЙК ----------
    elif call.data.startswith("like_"):
        poem_id = int(call.data.split("_")[1])
        cursor.execute("UPDATE poems SET likes = likes + 1 WHERE id=?", (poem_id,))
        conn.commit()

        bot.answer_callback_query(call.id, "Вы поставили лайк!")

        cursor.execute("SELECT likes, dislikes FROM poems WHERE id=?", (poem_id,))
        likes, dislikes = cursor.fetchone()

        bot.send_message(call.message.chat.id, f"👍 {likes}   👎 {dislikes}")

    # ---------- ДИЗЛАЙК ----------
    elif call.data.startswith("dislike_"):
        poem_id = int(call.data.split("_")[1])
        cursor.execute("UPDATE poems SET dislikes = dislikes + 1 WHERE id=?", (poem_id,))
        conn.commit()

        bot.answer_callback_query(call.id, "Вы поставили дизлайк!")

        cursor.execute("SELECT likes, dislikes FROM poems WHERE id=?", (poem_id,))
        likes, dislikes = cursor.fetchone()

        bot.send_message(call.message.chat.id, f"👍 {likes}   👎 {dislikes}")


# ================= FLASK =================
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is alive!"


def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)


# ================= RUN BOTH =================
def run_bot():
    print("BOT STARTED...")
    bot.infinity_polling(skip_pending=True)


# Flask в отдельном потоке
threading.Thread(target=run_flask, daemon=True).start()

# Telegram в главном потоке
run_bot()
