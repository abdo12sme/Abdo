import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "PUT_YOUR_BOT_TOKEN_HERE"
bot = telebot.TeleBot(TOKEN)

results = []  # قائمة لتخزين أسماء اللاعبين الفائزين

# 🏆 استقبال أسماء اللاعبين وتخزينها تلقائيًا
@bot.message_handler(func=lambda message: "," in message.text)
def store_results(message):
    players = [p.strip() for p in message.text.split(",")]
    results.extend(players)
    bot.send_message(message.chat.id, "✅ تم تسجيل الجولة! أرسل /predict لتحليل النتائج.")

# 🔮 تحليل بيانات اللاعبين وتوقع الفائز
@bot.message_handler(commands=['predict'])
def predict_winner(message):
    if not results:
        bot.send_message(message.chat.id, "❗ لا توجد بيانات كافية! أرسل بعض الجولات أولاً.")
        return

    # حساب نسب الفوز لكل لاعب
    stats = {player: results.count(player) / len(results) * 100 for player in set(results)}
    stats_sorted = sorted(stats.items(), key=lambda x: x[1], reverse=True)

    prediction_message = "🔮 **توقع الجولة القادمة:**\n"
    for player, percentage in stats_sorted:
        prediction_message += f"{player}: {percentage:.1f}%\n"

    bot.send_message(message.chat.id, prediction_message)

    # 🏆 إرسال الأزرار للاختيار
    markup = InlineKeyboardMarkup()
    for player, _ in stats_sorted:
        markup.add(InlineKeyboardButton(player, callback_data=player))

    bot.send_message(message.chat.id, "⚽ من الفائز الفعلي؟ اختر من الأزرار أدناه:", reply_markup=markup)

# 🏆 تحديث النتائج بعد ضغط الأزرار
@bot.callback_query_handler(func=lambda call: call.data in set(results))
def update_results(call):
    actual_winner = call.data
    results.append(actual_winner)

    bot.answer_callback_query(call.id, f"✅ تم تسجيل فوز {actual_winner}!")
    bot.send_message(call.message.chat.id, f"📊 تم تحديث الإحصائيات بناءً على فوز {actual_winner}. أرسل /predict لتحليل جديد!")

# 🚀 تشغيل البوت بشكل مستمر
bot.polling()
