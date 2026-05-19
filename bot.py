import telebot
from telebot import types
import config

bot = telebot.TeleBot(config.BOT_TOKEN)

# ==================== غُرْفَة التَّحَكُّم السِّيَادِيَّة ====================

# أَمْر البَدْء /start (يِشْتَغِل فِي الخَاص جَس)
@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.chat.type == 'private':
        welcome_text = (
            "⚙️ **مَرْحَبَاً بِك يَا بَاشْمُهَنْدِسْ فِي المَكْتَب الهَنْدَسي الذَّكِي!**\n\n"
            "مَشْرُوع (The Five Brains) جَاهِز ذَلْحِيْن وَمَرْبُوط بِالمَخْزَن السِّيَادِي.\n\n"
            "اضْغَط عَلَى /settings لِفَتْح لَوْحَة التَّحَكُّم الرَّئِيْسِيَّة."
        )
        bot.reply_to(message, welcome_text, parse_mode="Markdown")

# أَمْر الإِعْدَادَات /settings (لَوْحَة التَّحَكُّم بِالأَزْرَار)
@bot.message_handler(commands=['settings'])
def show_settings(message):
    if message.chat.type == 'private':
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_keys = types.InlineKeyboardButton("🔑 إِدَارَة مَفَاتِيْح الـ API", callback_data="manage_keys")
        btn_prompts = types.InlineKeyboardButton("📜 التَّوْجِيْهَات وَالسِّيَادَات (Prompts)", callback_data="manage_prompts")
        btn_status = types.InlineKeyboardButton("📊 حَالَة العُقُوْل الخَمْسَة", callback_data="bot_status")
        markup.add(btn_keys, btn_prompts, btn_status)
        
        bot.send_message(
            message.chat.id, 
            "🛠️ **غُرْفَة التَّحَكُّم الرَّئِيْسِيَّة لِلْمَشْرُوع:**\nاخْتَار البَنْد الَّذِي تِشْتِي تِهَنْدِسُه:", 
            reply_markup=markup, 
            parse_mode="Markdown"
        )

# ==================== الأَكْشَن وَالتَّفَاعُل مَعَ الأَزْرَار ====================
@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    if call.data == "manage_keys":
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("➕ إِضَافَة مِفْتَاح", callback_data="add_key"),
            types.InlineKeyboardButton("❌ حَذْف مِفْتَاح", callback_data="view_keys")
        )
        markup.add(types.InlineKeyboardButton("🔙 عَوْدَة", callback_data="main_menu"))
        bot.edit_message_text("🔑 **قَائِمَة إِدَارَة مَفَاتِيْح الـ API:**\n\nتِقْدِر ذَلْحِيْن تِصُبّ مَفَاتِيْح Gemini, OpenAI, Claude دَاخِل المَخْزَن.", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        
    elif call.data == "manage_prompts":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 عَوْدَة", callback_data="main_menu"))
        bot.edit_message_text("📜 **غُرْفَة السِّيَادَات وَالتَّوْجِيْهَات (Prompts):**\n\nهُنَا عَنِصُبّ التَّوْجِيه المِثَالِي لِكُلِّ عَقْل عِشَان يِشْتَغِل بِاللَّهْجَة وَالعِلْم المَطْلُوب.", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        
    elif call.data == "bot_status":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 عَوْدَة", callback_data="main_menu"))
        status_text = (
            "📊 **حَالَة المَشْرُوع الحَالِيَّة:**\n\n"
            "🔹 **المَخْزَن السِّيَادِي:** مَرْبُوط مِيْة المِيْة ✅\n"
            "🔹 **العُقُوْل الشَّغَّالَة:** جَاهِزَة لِلتَّهْيِئَة 🧠\n"
            "🔹 **نِظَام التَّشْغِيل:** Polling مُسْتَمِرّ ⚡"
        )
        bot.edit_message_text(status_text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        
    elif call.data == "main_menu":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🔑 إِدَارَة مَفَاتِيْح الـ API", callback_data="manage_keys"),
            types.InlineKeyboardButton("📜 التَّوْجِيْهَات وَالسِّيَادَات (Prompts)", callback_data="manage_prompts"),
            types.InlineKeyboardButton("📊 حَالَة العُقُوْل الخَمْسَة", callback_data="bot_status")
        )
        bot.edit_message_text("🛠️ **غُرْفَة التَّحَكُّم الرَّئِيْسِيَّة لِلْمَشْرُوع:**\nاخْتَار البَنْد الَّذِي تِشْتِي تِهَنْدِسُه:", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

# ==================== رَادَار الـ ID (لِلِاحْتِيَاط) ====================
@bot.message_handler(func=lambda message: message.text and message.text.strip().lower() in ['id', '/id'])
def reply_id(message):
    if message.chat.type in ['group', 'supergroup']:
        bot.reply_to(message, f"🎯 رَقَم المَجْمُوعَة مُثَبَّت فِي القَاعِدَة بِالْفِعْل:\n`{config.GROUP_DATABASE_ID}`", parse_mode="Markdown")

if __name__ == "__main__":
    print("المَكْتَب الهَنْدَسي الذَّكِي شَغَّال ذَلْحِيْن بِنَجَاح...")
    bot.infinity_polling()
