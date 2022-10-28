import requests
from bs4 import BeautifulSoup
import telebot
from telebot import types
import validators

bot = telebot.TeleBot('token') # change token!!!

def getPhoto(link):
    if not validators.url(link):
        return []
    else:
        receivedPhotos = []
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        images = soup.find_all('img', {"data-src": True})
        receivedPhotos.append((soup.find('img'))['src']) #add first photo
        for image in images:
            receivedPhotos.append(image['data-src']) #add latest photo
        return receivedPhotos

@bot.message_handler(commands=['start'])
def startInfo(message):
    bot.send_message(message.chat.id, '<b>Надішли боту посилання на оголошення з олх і він надішле тобі фото. 2022 RomanDydyk</b>\u2764', parse_mode='html')

@bot.message_handler()
def sendPhoto(message):
    try:
        link = message.text
        if getPhoto(link):
            medias = []
            for photo_ID in (getPhoto(link)):
                medias.append(types.InputMediaPhoto(photo_ID))
            if len(medias) <= 10: #if less than 10 photo
                bot.send_media_group(message.chat.id, media=medias)
            elif len(medias) <= 20: #if more than 10 photo
                bot.send_media_group(message.chat.id, media=medias[0:10])
                bot.send_media_group(message.chat.id, media=medias[11:20])
            else: #if more than 20 photo
                bot.send_media_group(message.chat.id, media=medias[0:10])
                bot.send_media_group(message.chat.id, media=medias[11:20])
                bot.send_media_group(message.chat.id, media=medias[21:30])
        else:
            bot.send_message(message.chat.id, 'Посилання не вірне, перевірте і відправте ще раз')
    except:
        bot.send_message(message.chat.id, 'Посилання не вірне, перевірте і відправте ще раз')

bot.polling(none_stop=True)


