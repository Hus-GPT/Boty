import telebot
from telebot import types
import config

bot = telebot.TeleBot(config.BOT_TOKEN)

@bot.message_handler(func=lambda message: message.chat.type in ['group', 'supergroup'])
def catch_group_id(message):
    if message.text and message.text.strip().lower() == 'id':
        group_id = message.chat.id
        reply_text = (
            f"🎯 **تِمّ لَقْط الـ ID بِنَجَاح يَا بَاشْمُهَنْدِسْ!**\n\n"
            f"رَقَم مَجْمُوعَتَك هُو:\n`{group_id}`\n\n"
            f"اِنْسَخه واِطْرَحه لِي في الشَّات عَشَان نِثَبِّته!"
        )
        bot.reply_to(message, reply_text, parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.chat.type == 'private':
        welcome_text = "⚙️ **المَكْتَب الهَنْدَسي الذَّكِي جَاهِز!**\n\nاضغط على /settings لِفَتْح غُرْفَة التَّحَكُّم."
        bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(commands=['settings'])
def show_settings(message):
    if message.chat.type == 'private':
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_keys = types.InlineKeyboardButton("🔑 إِدَارَة مَفَاتِيْح الـ API", callback_data="manage_keys")
        btn_prompts = types.InlineKeyboardButton("📜 التَّوْجِيْهَات والسِّيَادَات", callback_data="manage_prompts")
        markup.add(btn_keys, btn_prompts)
        bot.send_message(message.chat.id, "🛠️ **غُرْفَة التَّحَكُّم الرَّئِيْسِيَّة:**", reply_markup=markup, parse_mode="Markdown")

if __name__ == "__main__":
    bot.infinity_polling()
