import requests
from bs4 import BeautifulSoup as bs
import telebot as tb
from telebot import types

# Class for extracting information from a random wikipedia article
class Wikipedia:
    def __init__(self):
        self.random_URL = 'https://en.wikipedia.org/wiki/Special:Random' # link that opens a random wikipedia article
        self.article = requests.get(self.random_URL) # extracts the artcile
        self.soup = bs(self.article.content, 'html.parser') # creates beautiful soup object
        self.URL = self.get_URL()
        self.Title = self.get_Title()
        self.Body = self.get_Body()

    def get_URL(self): # extracts the URL of the random wikipedia article
        return self.article.url

    def get_Title(self): # extracts the title of the random wikipedia article
        return self.soup.find(class_='firstHeading').text

    def get_Body(self): # extracts the main body of the random wikipedia article
        Body = ''
        for part in self.soup.find('p'):
            Body += part.text
        return Body

TOKEN = ''
bot = tb.TeleBot(TOKEN,threaded=False)

#register function
@bot.message_handler(commands=['start','go'])
@bot.edited_message_handler(commands=['start','go'])
def welcome_message(message):
    # Collect user info
    name = str(message.from_user.first_name)
    print(message.chat.id,name)
    # define keyboard
    keyboard = tb.types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton(text="Let's go!", callback_data='Start')
    keyboard.row(item1)
    bot.send_message(message.chat.id, 'Hi ' + name + '! I send random Wikipedia artciles. Ready to start?',
                     reply_markup=keyboard)

#Callback data handler
@bot.callback_query_handler(func=lambda call:True)
def callback_handler(call):
    if call.data=='Start':
        # define keyboard
        keyboard = tb.types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton(text="Send another article", callback_data='Start')
        keyboard.row(item1)
        # start
        bot.send_message(call.message.chat.id, text='Sending... It may take a moment')
        # get the article
        Result = Wikipedia()
        print(Result.Title)
        #send the article
        bot.send_message(call.message.chat.id, 'Title: ' + Result.Title +'\n'+'\n'+Result.Body +'\n' + Result.URL,
                         reply_markup=keyboard)

#Text handler
@bot.message_handler(content_types=['text'])
@bot.edited_message_handler(content_types=['text'])
def reply(message):
    print(message.text) # Record incoming messages

bot.polling(none_stop=True) # starts the bot


############################## NOTES ##############################

# find(element_tag, attribute) #return first matching item
# find_all(element_tag, attribute) #return list of matching items
# print(soup.find(class_='media media--hero media--primary media--overlay block-link').get('data-bbc-title'))
# print(soup.prettify())
