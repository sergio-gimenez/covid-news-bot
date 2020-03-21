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
