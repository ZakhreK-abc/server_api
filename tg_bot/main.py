import telebot
import requests
from telebot import types

TOKEN = '8270290375:AAFPw1-N0V-S0Bx4OJlAtNu3QTOkSZM_Kqk'
bot = telebot.TeleBot(TOKEN)
API_URL = "http://192.168.111.101:5000"

# Хранилище данных пользователей
user_data = {}

# ==================== ГЛАВНОЕ МЕНЮ ====================
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton('🔍 Поиск'),
        types.KeyboardButton('📋 Все'),
        types.KeyboardButton('➕ Добавить'),
        types.KeyboardButton('✏️ Обновить'),
        types.KeyboardButton('❌ Удалить')
    )
    bot.send_message(message.chat.id, "📁 **Меню БД**", reply_markup=markup, parse_mode='Markdown')

# ==================== ПОИСК ====================
@bot.message_handler(func=lambda m: m.text == '🔍 Поиск')
def search_menu(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📛 Имя", callback_data="search_name"),
        types.InlineKeyboardButton("🏷️ Тип", callback_data="search_type"),
        types.InlineKeyboardButton("⚡ Статус", callback_data="search_status"),
        types.InlineKeyboardButton("◀️ Назад", callback_data="back")
    )
    bot.send_message(message.chat.id, "🔍 **Поиск по:**", reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda c: c.data == 'search_name')
def search_name(call):
    bot.edit_message_text("📛 Введите имя:", call.message.chat.id, call.message.message_id)
    bot.register_next_step_handler(call.message, process_search_name)

@bot.callback_query_handler(func=lambda c: c.data == 'search_type')
def search_type(call):
    bot.edit_message_text("🏷️ Введите тип:", call.message.chat.id, call.message.message_id)
    bot.register_next_step_handler(call.message, process_search_type)

@bot.callback_query_handler(func=lambda c: c.data == 'search_status')
def search_status(call):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("✅ 1", callback_data="status_1"),
        types.InlineKeyboardButton("❌ 0", callback_data="status_0")
    )
    bot.edit_message_text("⚡ Выберите статус:", call.message.chat.id, call.message.message_id, reply_markup=markup)

def process_search_name(message):
    try:
        res = requests.get(f"{API_URL}/api/db/name/{message.text}")
        data = res.json()
        if data:
            msg = "🔍 **Результат:**\n\n"
            for i in data:
                msg += f"🆔 {i[0]} | 📛 {i[1]} | 🔢 {i[2]} |\n| 🗒️ {i[3]} | 🗓️ {i[4]} |\n| 🗂️ {i[5]} | ⚡ {'✅' if i[6]==1 else '❌'}\n\n"
        else:
            msg = "❌ Ничего не найдено"
        bot.send_message(message.chat.id, msg, parse_mode='Markdown')
    except:
        bot.send_message(message.chat.id, "❌ Ошибка")

def process_search_type(message):
    try:
        res = requests.get(f"{API_URL}/api/db/type/{message.text}")
        data = res.json()
        if data:
            msg = "🔍 **Результат:**\n\n"
            for i in data:
                msg += f"🆔 {i[0]} | 📛 {i[1]} | 🔢 {i[2]} |\n| 🗒️ {i[3]} | 🗓️ {i[4]} |\n| 🗂️ {i[5]} | ⚡ {'✅' if i[6]==1 else '❌'}\n\n"
        else:
            msg = "❌ Ничего не найдено"
        bot.send_message(message.chat.id, msg, parse_mode='Markdown')
    except:
        bot.send_message(message.chat.id, "❌ Ошибка")

@bot.callback_query_handler(func=lambda c: c.data in ['status_0', 'status_1'])
def process_status(call):
    try:
        status = call.data.split('_')[1]
        res = requests.get(f"{API_URL}/api/db/status/{status}")
        data = res.json()
        if data:
            msg = f"🔍 **Статус {status}:**\n\n"
            for i in data:
                msg += f"🆔 {i[0]} | 📛 {i[1]} | 🔢 {i[2]} |\n| 🗒️ {i[3]} | 🗓️ {i[4]} |\n| 🗂️ {i[5]} | ⚡ {'✅' if i[6]==1 else '❌'}\n\n"
        else:
            msg = "❌ Ничего не найдено"
        bot.edit_message_text(msg, call.message.chat.id, call.message.message_id, parse_mode='Markdown')
    except:
        bot.edit_message_text("❌ Ошибка", call.message.chat.id, call.message.message_id)

# ==================== ВСЕ ЗАПИСИ ====================
@bot.message_handler(func=lambda m: m.text == '📋 Все')
def get_all(message):
    try:
        res = requests.get(f"{API_URL}/api/db/0")
        data = res.json()
        if data:
            msg = "📋 **Все записи:**\n\n"
            for i in data:
                msg += f"🆔 {i[0]} | 📛 {i[1]} | ⚡ {'✅' if i[6]==1 else '❌'}\n"
        else:
            msg = "📭 База пуста"
        bot.send_message(message.chat.id, msg, parse_mode='Markdown')
    except:
        bot.send_message(message.chat.id, "❌ Ошибка")

# ==================== ДОБАВЛЕНИЕ ====================
@bot.message_handler(func=lambda m: m.text == '➕ Добавить')
def add_start(message):
    msg = bot.send_message(message.chat.id, "📛 Введите имя:")
    bot.register_next_step_handler(msg, add_name)
    user_data[message.chat.id] = {}

def add_name(message):
    user_data[message.chat.id]['name'] = message.text
    msg = bot.send_message(message.chat.id, "🔢 Введите число:")
    bot.register_next_step_handler(msg, add_number)

def add_number(message):
    try:
        user_data[message.chat.id]['number'] = int(message.text)
        msg = bot.send_message(message.chat.id, "📝 Введите заметку:")
        bot.register_next_step_handler(msg, add_note)
    except:
        bot.send_message(message.chat.id, "❌ Ошибка, введите число:")
        bot.register_next_step_handler(message, add_number)

def add_note(message):
    user_data[message.chat.id]['note'] = message.text
    msg = bot.send_message(message.chat.id, "🏷️ Введите тип:")
    bot.register_next_step_handler(msg, add_type)

def add_type(message):
    user_data[message.chat.id]['type'] = message.text
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("✅ 1", callback_data="add_status_1"),
        types.InlineKeyboardButton("❌ 0", callback_data="add_status_0")
    )
    bot.send_message(message.chat.id, "⚡ Выберите статус:", reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data.startswith('add_status_'))
def add_status(call):
    user_data[call.message.chat.id]['status'] = int(call.data.split('_')[2])
    try:
        res = requests.post(f"{API_URL}/api/db", json=user_data[call.message.chat.id])
        if res.status_code == 200:
            bot.edit_message_text("✅ **Запись добавлена!**", call.message.chat.id, call.message.message_id, parse_mode='Markdown')
        else:
            bot.edit_message_text("❌ Ошибка", call.message.chat.id, call.message.message_id)
    except:
        bot.edit_message_text("❌ Ошибка", call.message.chat.id, call.message.message_id)
    del user_data[call.message.chat.id]

# ==================== ОБНОВЛЕНИЕ ====================
@bot.message_handler(func=lambda m: m.text == '✏️ Обновить')
def update_start(message):
    msg = bot.send_message(message.chat.id, "🆔 Введите ID для обновления:")
    bot.register_next_step_handler(msg, update_id)
    user_data[message.chat.id] = {}

def update_id(message):
    try:
        user_data[message.chat.id]['id'] = int(message.text)
        msg = bot.send_message(message.chat.id, "📛 Новое имя (или '-'):")
        bot.register_next_step_handler(msg, update_name)
    except:
        bot.send_message(message.chat.id, "❌ Ошибка, введите число:")
        bot.register_next_step_handler(message, update_id)

def update_name(message):
    if message.text != '-':
        user_data[message.chat.id]['name'] = message.text
    msg = bot.send_message(message.chat.id, "🔢 Новое число (или '-'):")
    bot.register_next_step_handler(msg, update_number)

def update_number(message):
    if message.text != '-':
        try:
            user_data[message.chat.id]['number'] = int(message.text)
        except:
            bot.send_message(message.chat.id, "❌ Ошибка, введите число:")
            bot.register_next_step_handler(message, update_number)
            return
    msg = bot.send_message(message.chat.id, "📝 Новая заметка (или '-'):")
    bot.register_next_step_handler(msg, update_note)

def update_note(message):
    if message.text != '-':
        user_data[message.chat.id]['note'] = message.text
    msg = bot.send_message(message.chat.id, "🏷️ Новый тип (или '-'):")
    bot.register_next_step_handler(msg, update_type)

def update_type(message):
    if message.text != '-':
        user_data[message.chat.id]['type'] = message.text
    msg = bot.send_message(message.chat.id, "⚡ Новый статус 0/1 (или '-'):")
    bot.register_next_step_handler(msg, update_status)

def update_status(message):
    if message.text != '-':
        try:
            user_data[message.chat.id]['status'] = int(message.text)
        except:
            bot.send_message(message.chat.id, "❌ Ошибка, введите 0 или 1:")
            bot.register_next_step_handler(message, update_status)
            return
    
    uid = user_data[message.chat.id].pop('id')
    try:
        res = requests.put(f"{API_URL}/api/db/id/{uid}", json=user_data[message.chat.id])
        if res.status_code == 200:
            bot.send_message(message.chat.id, f"✅ **Запись {uid} обновлена!**", parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, "❌ Ошибка")
    except:
        bot.send_message(message.chat.id, "❌ Ошибка")
    del user_data[message.chat.id]

# ==================== УДАЛЕНИЕ ====================
@bot.message_handler(func=lambda m: m.text == '❌ Удалить')
def delete_start(message):
    msg = bot.send_message(message.chat.id, "🆔 Введите ID для удаления:")
    bot.register_next_step_handler(msg, delete_id)

def delete_id(message):
    try:
        res = requests.delete(f"{API_URL}/api/db/id/{int(message.text)}")
        if res.status_code == 200:
            bot.send_message(message.chat.id, f"✅ **Запись {message.text} удалена!**", parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, "❌ Запись не найдена")
    except:
        bot.send_message(message.chat.id, "❌ Ошибка")

# ==================== НАЗАД ====================
@bot.callback_query_handler(func=lambda c: c.data == 'back')
def back(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    start(call.message)

# ==================== ЗАПУСК ====================
if __name__ == "__main__":
    print("🤖 Бот запущен...")
    bot.infinity_polling()