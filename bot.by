import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from collections import deque

# ⚠️ استخدم التوكن بحذر، لا تنشر هذا الكود في أماكن عامة!
TOKEN = "8196612850:AAGbcphDaSY0SNSOXaJdxllTGQ57TKweeQ4"
bot = telebot.TeleBot(TOKEN)

# تخزين جميع الجولات بدون حد أقصى
results = []

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🎮 مرحبًا! أرسل أسماء الفائزين في كل جولة، وسأحلل الأنماط باستمرار.")

@bot.message_handler(commands=['predict'])
def predict_winner(message):
    if not results:
        bot.send_message(message.chat.id, "❗ لا توجد بيانات كافية! أرسل بعض الجولات أولاً.")
        return

    # حساب نسب الفوز لكل لاعب بناءً على كل الجولات المخزنة
    stats = {player: results.count(player) / len(results) * 100 for player in set(results)}
    stats_sorted = sorted(stats.items(), key=lambda x: x[1], reverse=True)

    prediction_message = "🔮 **توقع الجولة القادمة:**\n"
    for player, percentage in stats_sorted:
        prediction_message += f"{player}: {percentage:.1f}%\n"

    bot.send_message(message.chat.id, prediction_message)

    # إرسال الأزرار لاختيار الفائز الفعلي
    markup = InlineKeyboardMarkup()
    for player in set(results):
        markup.add(InlineKeyboardButton(player, callback_data=player))
    
    bot.send_message(message.chat.id, "⚽ من الفائز الفعلي؟ اختر من الأزرار أدناه:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in set(results))
def update_results(call):
    actual_winner = call.data
    results.append(actual_winner)

    bot.answer_callback_query(call.id, f"✅ تم تسجيل فوز {actual_winner}!")
    bot.send_message(call.message.chat.id, f"📊 تم تحديث الإحصائيات بناءً على فوز {actual_winner}. أرسل /predict لتحليل جديد!")

bot.polling()