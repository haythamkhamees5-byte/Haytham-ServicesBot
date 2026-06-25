import telebot
from telebot import types
import json
import os
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

# دالة لقراءة الأسعار من ملف JSON
def load_prices():
    if os.path.exists('prices.json'):
        with open('prices.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"key_1": "10", "key_2": "20", "key_3": "30"}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    prices = load_prices()
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    # الأزرار مع الأسعار المستقاة من الملف
    btn1 = types.InlineKeyboardButton(f"مفتاح تفعيل 1 شهر 🔑 ({prices.get('key_1')}$) ", callback_data="buy_key_1")
    btn2 = types.InlineKeyboardButton(f"مفتاح تفعيل 3 أشهر 🔑 ({prices.get('key_2')}$) ", callback_data="buy_key_2")
    btn3 = types.InlineKeyboardButton(f"مفتاح تفعيل 6 أشهر 🔑 ({prices.get('key_3')}$) ", callback_data="buy_key_3")
    btn_support = types.InlineKeyboardButton("الدعم الفني والوكلاء 👨‍💻", callback_data="support")
    
    markup.add(btn1, btn2, btn3, btn_support)
    
    welcome_text = (
        "مرحباً بك في بوت الخدمات المطور 🤖✨\n\n"
        "يمكنك من خلال هذا البوت شراء مفاتيح التفعيل المعتمدة بكل سهولة وبشكل أوتوماتيكي.\n"
        "يرجى اختيار الخدمة المطلوبة من الأزرار أدناه:"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data.startswith("buy_key_"):
        key_type = call.data.split("_")[-1]
        prices = load_prices()
        price = prices.get(f"key_{key_type}", "0")
        
        text = (
            f"لقد اخترت شراء مفتاح تفعيل (خيار {key_type})\n"
            f"السعر الحالي: {price}$\n\n"
            "لإتمام عملية الدفع واستلام المفتاح فوراً، يرجى التواصل مع الإدارة عبر الدعم الفني."
        )
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text)
        
    elif call.data == "support":
        support_text = (
            "👨‍💻 لقسم الدعم الفني والاستفسارات أو شحن الرصيد:\n\n"
            "يرجى التواصل مباشرة مع المطور: @Haitham_Khamees\n"
            "نحن هنا لخدمتك على مدار الساعة!"
        )
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=support_text)

if __name__ == "__main__":
    print("البوت يعمل الآن بنجاح...")
    bot.infinity_polling()
