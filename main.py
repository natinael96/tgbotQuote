import requests
import telebot
import random
import time
import json
from io import BytesIO
import textwrap

TOKEN = '7121923647:AAHS2806Xb-6Ic_zLZtF49JWugdwd0SEPoE'  # bot token
bot = telebot.TeleBot(TOKEN)  # bot instance

group_id = '-1002140605617'  # group id
quote_file = 'quotes.json'  # JSON file containing quotes
posted_file = 'posted.json'  # JSON file to keep track of posted quotes

def load_quotes():
    """Loads quotes from the JSON file."""
    with open(quote_file, 'r') as file:
        quotes = json.load(file)
    return quotes

def load_posted():
    """Loads posted quotes from the JSON file."""
    try:
        with open(posted_file, 'r') as file:
            posted = json.load(file)
    except FileNotFoundError:
        posted = []
    return posted

def save_posted(posted):
    """Saves posted quotes to the JSON file."""
    
    with open(posted_file, 'w') as file:
        json.dump(posted, file, indent=4)

def get_random_quote(quotes, posted):
    """Picks a random quote from the list of quotes that hasn't been posted yet."""
    available_quotes = [q for q in quotes if q not in posted]
    if available_quotes:
        return random.choice(available_quotes)
    else:
        # If all quotes have been posted, reset the posted list
        save_posted([])
        return random.choice(quotes)

def publish_daily_quote():
    """Publishes a daily quote to the Telegram group."""
    quotes = load_quotes()
    posted = load_posted()
    
    quote = get_random_quote(quotes, posted)
    
    if quote:
        quote_text = quote['quote']
        author = quote['author']
        # wrap text
        wrapped_text = textwrap.fill(quote_text, width=50)
        
        message = f'"{wrapped_text}"\n\n- {author}'
        bot.send_message(group_id, message)
        
        # Save the posted quote
        posted.append(quote)
        save_posted(posted)
    else:
        bot.send_message(group_id, 'Failed to fetch daily quote')

while True:
    publish_daily_quote()
    time.sleep(86400)