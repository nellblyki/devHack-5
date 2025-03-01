from g4f.client import Client as G4FClient
from g4f import models
import telebot
import requests
from bs4 import BeautifulSoup

TOKEN = '8040057324:AAGyYxti9hozirDbImTAIKMNg1ySKC4nobk'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
  bot.send_message(message.chat.id, 'Здравствуйте ' + message.from_user.first_name)

@bot.message_handler(content_types=['text'])
def text(message):

  url = 'https://sfedu.ru/'
  r = requests.get(url)
  data = BeautifulSoup(r.text).text.replace('\n', '')

  text = message.text
  text += data

  promt = 'Ты помощник-ассистент для Университета ЮФУ. Отвечай на все сообщения вежливо и на русском языке'
  client = G4FClient()
  response = client.chat.completions.create(
      model="gpt-4o",
      messages=[{"role": "user", "content": f'{promt}\n{text}'}],
  )
  bot.send_message(message.chat.id, response.choices[0].message.content)

bot.polling()
