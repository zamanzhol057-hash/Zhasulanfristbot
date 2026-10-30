
import os
import random
import re
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

# =========================
# НАСТРОЙКИ ИГРЫ
# =========================

COUNTRIES = {
    "Казахстан": "Астана",
    "Франция": "Париж",
    "Япония": "Токио",
    "Италия": "Рим",
    "Германия": "Берлин",
    "Испания": "Мадрид",
    "Китай": "Пекин",
    "Россия": "Москва",
    "Турция": "Анкара",
    "Египет": "Каир",
    "Канада": "Оттава",
    "Бразилия": "Бразилиа",
    "Австралия": "Канберра",
    "Южная Корея": "Сеул",
    "Аргентина": "Буэнос-Айрес",
}

JOKES = [
    "Почему географ не теряется? Потому что всегда знает координаты!",
    "Почему глобус не спорит? У него весь мир перед глазами!",
    "Что сказал океан берегу? Ничего, просто помахал волной!",
    "Почему карта получила хорошую оценку? Потому что знала все стороны света!",
]

FACTS = [
    "🇰🇿 Астана — столица Казахстана. Зимой здесь бывает очень холодно.",
    "🇫🇷 Париж — столица Франции. Здесь находится знаменитая Эйфелева башня.",
    "🇯🇵 Токио — столица Японии и один из крупнейших городских центров мира.",
    "🇮🇹 Рим — столица Италии. Внутри Рима находится независимое государство Ватикан.",
    "🇬🇧 Лондон — столица Великобритании. Через город протекает река Темза.",
    "🇪🇬 Каир — столица Египта. Недалеко от города находятся знаменитые пирамиды Гизы.",
    "🇹🇷 Анкара — столица Турции, а не Стамбул.",
    "🇦🇺 Канберра — столица Австралии. Её выбрали в качестве столицы между Сиднеем и Мельбурном.",
    "🇧🇷 Бразилиа — столица Бразилии. Город был официально открыт в 1960 году.",
    "🇨🇦 Оттава — столица Канады. Город расположен в провинции Онтарио.",
]

# =========================
# КНОПКИ
# =========================

reply_keyboard = ReplyKeyboardMarkup(
    [
        ["🌍 Столицы стран", "🆘 Help"],
        ["😂 Joke", "🌎 Факты о странах"],
    ],
    resize_keyboard=True,
)

inline_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                "ℹ️ Что умеет бот?",
                callback_data="help",
            )
        ]
    ]
)

# =========================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# =========================

def normalize(text: str) -> str:
    """Убирает лишние пробелы и знаки, приводит текст к нижнему регистру."""
    return re.sub(r"[^\w\s-]", "", text.casefold()).strip()


# =========================
# КОМАНДА /START
# =========================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    context.user_data["current_country"] = None

    await update.message.reply_text(
        "Привет! 👋 Добро пожаловать в географическую викторину!\n\n"
        "Выбирай, что хочешь делать:",
        reply_markup=reply_keyboard,
    )

    await update.message.reply_text(
        "Нажми кнопку ниже, чтобы узнать о моих возможностях.",
        reply_markup=inline_keyboard,
    )


# =========================
# HELP
# =========================

async def show_help(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    await update.message.reply_text(
        "🆘 Я бот-викторина по географии!\n\n"
        "🌍 Столицы стран — угадывай столицы разных стран.\n"
        "😂 Joke — читай шутки о географии.\n"
        "🌎 Факты о странах — узнавай интересные факты.\n\n"
        "За правильные ответы ты получаешь очки. Удачи!"
    )


# =========================
# INLINE-КНОПКА
# =========================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query
    await query.answer()

    if query.data == "help":
        await query.message.reply_text(
            "ℹ️ Я географический бот!\n\n"
            "Я задаю вопросы о столицах стран, "
            "рассказываю интересные факты и шутки."
        )


# =========================
# ИГРА В СТОЛИЦЫ
# =========================

async def capitals_game(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    context.user_data["current_country"] = None

    asked = context.user_data.setdefault("asked_countries", [])

    available = [
        country for country in COUNTRIES
        if country not in asked
    ]

    if not available:
        asked.clear()
        available = list(COUNTRIES.keys())

    country = random.choice(available)
    asked.append(country)

    context.user_data["current_country"] = country

    await update.message.reply_text(
        f"🌍 Назови столицу страны: {country}"
    )


# =========================
# JOKE
# =========================

async def show_joke(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    await update.message.reply_text(
        "😂 Географическая шутка:\n\n"
        + random.choice(JOKES)
    )


# =========================
# ФАКТЫ О СТРАНАХ
# =========================

async def show_facts(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    await update.message.reply_text(
        "🌎 Интересный факт:\n\n"
        + random.choice(FACTS)
    )


# =========================
# ОБРАБОТКА ОТВЕТОВ И КНОПОК
# =========================

async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    text = update.message.text.strip()

    # Проверяем нажатия Reply-кнопок
    if text == "🌍 Столицы стран":
        await capitals_game(update, context)
        return

    if text == "🆘 Help":
        await show_help(update, context)
        return

    if text == "😂 Joke":
        await show_joke(update, context)
        return

    if text == "🌎 Факты о странах":
        await show_facts(update, context)
        return

    # Если игрок отвечает на вопрос о столице
    country = context.user_data.get("current_country")

    if country is None:
        await update.message.reply_text(
            "Выбери действие с помощью кнопок меню. 😊"
        )
        return

    correct_answer = COUNTRIES[country]

    if normalize(text) == normalize(correct_answer):
        points = context.user_data.get("points", 0) + 1
        context.user_data["points"] = points
        context.user_data["current_country"] = None

        await update.message.reply_text(
            f"✅ Правильно! Столица страны {country} — "
            f"{correct_answer}!\n\n"
            f"🏆 Твои очки: {points}\n\n"
            "Нажми «🌍 Столицы стран», чтобы продолжить."
        )
    else:
        context.user_data["current_country"] = None

        await update.message.reply_text(
            f"❌ Не совсем правильно!\n"
            f"Столица страны {country} — {correct_answer}.\n\n"
            "Нажми «🌍 Столицы стран», чтобы попробовать ещё раз."
        )


# =========================
# ЗАПУСК БОТА
# =========================

def main():
    token ="8972920668:AAEKJE29FNQc9DT_BNR2Grn6CZEH82fXVIE"

    if not token:
        raise RuntimeError(
            "Не найден BOT_TOKEN. Укажи токен в переменной окружения."
        )

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", show_help))
    app.add_handler(CommandHandler("joke", show_joke))

    app.add_handler(CallbackQueryHandler(button_handler))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message,
        )
    )

    print("Бот запущен!")
    app.run_polling()


if __name__ == "__main__":
    main()