from telegram.ext import Updater, CommandHandler
import requests
import re

# This bot should return a dog image when we send the /bop command. To be able to do this, 
# we can use the public API from RandomDog to help us generate random dog images.

# The workflow of our bot is as simple as this:
# access the API -> get the image URL -> send the image
contents = requests.get('https://random.dog/woof.json').json()

# Get the image URL since we need that parameter to be able to send the image.
def get_url():
    contents = requests.get('https://random.dog/woof.json').json()    
    url = contents['url']
    return url

def perro(bot, update):
    # Get the url from the json
    url = get_url()

    # Get the recipient’s ID using this code:
    chat_id = update.message.chat_id

    # After we get the image URL and the recipient’s ID,
    # it’s time to send the message, which is an image.
    bot.send_photo(chat_id=chat_id, photo=url)


def main():
    updater = Updater('1070393137:AAGT8AVf0jWRYnVrnvsxkTlQtPqXLjwz2qU')
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('perro',perro))
    updater.start_polling()
    updater.idle()
    
if __name__ == '__main__':
    main()