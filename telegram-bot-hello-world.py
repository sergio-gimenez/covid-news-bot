# import logging
#
# from telegram import ReplyKeyboardMarkup
# from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
#                           ConversationHandler)
#
# import requests
# import re
#
#
# CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)
#
# # This bot should return a dog image when we send the /bop command. To be able to do this,
# # we can use the public API from RandomDog to help us generate random dog images.
#
# # The workflow of our bot is as simple as this:
# # access the API -> get the image URL -> send the image
# contents = requests.get('https://random.dog/woof.json').json()
#
# # Get the image URL since we need that parameter to be able to send the image.
# def get_url():
#     contents = requests.get('https://random.dog/woof.json').json()
#     url = contents['url']
#     return url
#
# def add_information(bot, update):
#     # Get the url from the json
#     url = get_url()
#
#     # Get the recipient’s ID using this code:
#     chat_id = update.message.chat_id
#     print("Hola")
#     bot.send_message(chat_id=chat_id, text= "Quien eres? Ej: Bruno Ibáñez López")
#
#
#
# def main():
#     updater = Updater('1070393137:AAGT8AVf0jWRYnVrnvsxkTlQtPqXLjwz2qU')
#     dp = updater.dispatcher
#     conv_handler = ConversationHandler
#     dp.add_handler(CommandHandler('AddInfo',add_information))
#     updater.start_polling()
#     updater.idle()
#
# if __name__ == '__main__':
#     main()


"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE, SEND_INFO_TO_VALIDATE, IS_IT_TRUE , WHY_TRUST_YOU = range(6)

reply_keyboard = [['Información última hora', 'Información tiempo real'],
                  ['Validar/Desmentir información'],
                  ['Nada más']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])


def start(update, context):
    update.message.reply_text(
        "Hola! Somos una asociación sin ánimo de lucro que vela por la información verídica en épocas de FakeNews en Twitter y cadenas de mensajes",
        reply_markup=markup)

    return CHOOSING


def regular_choice(update, context):
    text = update.message.text
    context.user_data['choice'] = text
    update.message.reply_text(
        'Your {}? Yes, I would love to hear about that!'.format(text.lower()))

    return TYPING_REPLY


def received_information(update, context):
    user_data = context.user_data
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']

    update.message.reply_text("Neat! Just so you know, this is what you already told me:"
                              "{} You can tell me more, or change your opinion"
                              " on something.".format(facts_to_str(user_data)),
                              reply_markup=markup)

    return CHOOSING




def get_information(update, context):

    return SEND_INFO_TO_VALIDATE


def get_text_to_validate(update, context):
    text = update.message.text
    user_data = context.user_data
    name = update.message.from_user.name
    if user_data["true_or_false"] == True:
        if user_data["validated"] == None:
            user_data["validated"] == []
        user_data["validated"].append(update.message.text)
    else:
        if user_data["denied"] == None:
            user_data["denied"] == []
        user_data["denied"].append(update.message.text)
    update.message.reply_text("Esta información ha sido añadida al algoritmo".format(facts_to_str(user_data)),
                                  reply_markup=markup)

    if user_data["who_it_is"] == None:
        update.message.reply_text("{}, dínos quien eres para así poder tener en cuenta tu información".format(facts_to_str(name)))
        user_data["name"] = name
        return WHY_TRUST_YOU

    return IS_IT_TRUE

def is_true_or_false(update, context):
    update.message.reply_text("Envíanos un link que hayas recibido, una cadena de mensajes o un tweet y lo tendremos en cuenta en nuestro algoritmo")
    return CHOOSING

def who_you_are(update, context):
    text = update.message.text
    user_data["who_it_is"] = text

    update.message.reply_text("Gracias por tu información!")

    return

def validate_information(update, context):
    update.message.reply_text('Quieres validar o desmentir una información? ')
    return IS_IT_TRUE




def custom_choice(update, context):
    update.message.reply_text('Alright, please send me the category first, '
                              'for example "Most impressive skill"')

    return TYPING_CHOICE



def done(update, context):
    user_data = context.user_data
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text("I learned these facts about you:"
                              "{}"
                              "Until next time!".format(facts_to_str(user_data)))

    user_data.clear()
    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater('1028487474:AAGytwWBUqEQ_X_fY72zN7lWJQDXHo0tFMg', use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CHOOSING: [MessageHandler(Filters.regex('^Información última hora$'),
                                      get_information),
                       MessageHandler(Filters.regex('^Validar/Desmentir información$'),
                                      validate_information)
                       ],

            SEND_INFO_TO_VALIDATE: [MessageHandler(Filters.text,
                                           get_text_to_validate)
                            ],

            IS_IT_TRUE: [MessageHandler(Filters.regex('^Cierto/True/Falso/False$'),
                                             is_true_or_false)],

            WHY_TRUST_YOU: [MessageHandler(Filters.text,
                                           who_you_are)
                            ],

            TYPING_CHOICE: [MessageHandler(Filters.text,
                                           regular_choice)
                            ],

            TYPING_REPLY: [MessageHandler(Filters.text,
                                          received_information),
                           ],

        },

        fallbacks=[MessageHandler(Filters.regex('^Nada más$'), done)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
