main.py￼Enterimport telebot
from telebot import types
import os

TOKEN = os.environ['TOKEN']
bot = telebot.TeleBot(TOKEN)

user_scores = {}

questions = [
    {
        "question": "What is Pepe Elf’s main chain? 🐸🌲",
        "options": ["Alvey", "Solana", "Ethereum", "Bitcoin"],
        "answer": "Solana"
    },
    {
        "question": "What does $PELF stand for? 🐸✨",
        "options": ["Pepe Elf Token", "Perfect Elf Fund", "Pepe’s Legendary Frog", "Play Every Little Frog"],
        "answer": "Pepe Elf Token"
    },
    {
        "question": "Who helps Pepe Elf in the Forest? 🌲",
        "options": ["Vault Visionary", "Santa", "Froggies", "All of the above"],
        "answer": "All of the above"
    },
    {
        "question": "What emoji best represents Pepe Elf? 🐸✨",
        "options": ["🐸", "🦊", "🧝‍♂️", "🐱"],
        "answer": "🐸"
    },
]

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Welcome to the Pepe Elf Forest! 🐸✨\nType /quiz to start a trivia challenge!")

@bot.message_handler(commands=['quiz'])
def start_quiz(message):
    chat_id = message.chat.id
    user_scores[chat_id] = 0
    send_question(chat_id, 0)

def send_question(chat_id, q_index):
    if q_index < len(questions):
        q = questions[q_index]
        markup = types.InlineKeyboardMarkup()
        for option in q['options']:
            markup.add(types.InlineKeyboardButton(option, callback_data=f"{q_index}|{option}"))
        bot.send_message(chat_id, f"🐸 Question {q_index+1}: {q['question']}", reply_markup=markup)
    else:
        bot.send_message(chat_id, f"Quiz complete! 🎉 Your score: {user_scores.get(chat_id,0)}/{len(questions)} 🐸✨")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    q_index, selected = call.data.split("|")
    q_index = int(q_index)
    correct_answer = questions[q_index]['answer']

    if selected == correct_answer:
        bot.answer_callback_query(call.id, "✅ Correct!")
        user_scores[chat_id] += 1
    else:
        bot.answer_callback_query(call.id, f"❌ Wrong! Correct answer: {correct_answer}")

    send_question(chat_id, q_index + 1)

bot.polling()
