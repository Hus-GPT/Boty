import telebot
from telebot import types
import config

# تشغيل البوت المباشر بدون ويب هوك ولا فلسك
bot = telebot.TeleBot(config.BOT_TOKEN)

# رادار لقط الـ ID عبر أمر /id أو كلمة id عادية
@bot.message_handler(func=lambda message: True)
def catch_everything(message):
    # إذا كتبوا id أو /id داخل المجموعة
    if message.text and (message.text.strip().lower() == 'id' or message.text.strip().lower() == '/id'):
        if message.chat.type in ['group', 'supergroup']:
            group_id = message.chat.id
            reply_text = (
                f"🎯 **تِمّ لَقْط الـ ID بِنَجَاح يَا بَاشْمُهَنْدِسْ!**\n\n"
                f"رَقَم مَجْمُوعَتَك هُو:\n`{group_id}`\n\n"
                f"اِنْسَخه واِطْرَحه لِي فِي الشَّات عِنْد بَن جَابِر."
            )
            bot.reply_to(message, reply_text, parse_mode="Markdown")

if __name__ == "__main__":
    print("البوت الجديد شغال ذلحين ومستعد للقط الإشارة...")
    bot.infinity_polling()
