import os
import telebot
from telebot import types
from flask import Flask, request
import config

bot = telebot.TeleBot(config.BOT_TOKEN)
app = Flask(__name__)  # هِذا هُو الـ app الَّذِي تِدَوِّر عَلَيْه منصة Vercel!

# رَادَار لَقْط الـ ID دَاخل المَجْمُوعَات
@bot.message_handler(func=lambda message: message.chat.type in ['group', 'supergroup'])
def catch_group_id(message):
    if message.text and message.text.strip().lower() == 'id':
        group_id = message.chat.id
        reply_text = (
            f"🎯 **تِمّ لَقْط الـ ID بِنَجَاح يَا بَاشْمُهَنْدِسْ!**\n\n"
            f"رَقَم مَجْمُوعَتَك هُو:\n`{group_id}`\n\n"
            f"اِنْسَخه واِطْرَحه لِي في الشَّات عِند بَن جَابِر."
        )
        bot.reply_to(message, reply_text, parse_mode="Markdown")

# أَمْر البَدْء /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.chat.type == 'private':
        welcome_text = "⚙️ **المَكْتَب الهَنْدَسي الذَّكِي جَاهِز!**\n\nاضغط على /settings لِفَتْح غُرْفَة التَّحَكُّم."
        bot.reply_to(message, welcome_text, parse_mode="Markdown")

# لوحة التحكم /settings
@bot.message_handler(commands=['settings'])
def show_settings(message):
    if message.chat.type == 'private':
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_keys = types.InlineKeyboardButton("🔑 إِدَارَة مَفَاتِيْح الـ API", callback_data="manage_keys")
        btn_prompts = types.InlineKeyboardButton("📜 التَّوْجِيْهَات والسِّيَادَات", callback_data="manage_prompts")
        markup.add(btn_keys, btn_prompts)
        bot.send_message(message.chat.id, "🛠️ **غُرْفَة التَّحَكُّم الرَّئِيْسِيَّة:**", reply_markup=markup, parse_mode="Markdown")

# المَنْفَذ الرَّئِيْسِي لِاسْتِقْبَال رَسَائل Vercel (Webhook)
@app.route('/' + config.BOT_TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    # نِرْبُط الويب هوك تِلْقَائِيَّاً بِرَابِط السِّيرْفَر (يِتِمّ تَهْيِئَته لاحقاً أو يِشْتَغِل كَـ فَنكْشِن)
    return "<h1>البوت شغال والـ app جاهز مية المية!</h1>", 200

if __name__ == "__main__":
    # لِلْتَّشْغِيل المَحَلِّي لَوْ تَحْتَاج، لَكِن في Vercel هُوَ عَيَقْرَأ الـ app تِلْقَائِيَّاً
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
