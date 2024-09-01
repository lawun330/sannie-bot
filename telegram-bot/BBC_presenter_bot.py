# import libraries
import logging

import requests
import telebot

# declare constants
BOT_TOKEN = '7106413986:AAGBfO5T0ZP0RIsfXlSVLLwP72N1Z2OWbdo'
WEATHER_TOKEN = 'f1a839dc52704f43a9fd17f2903ac362'

# initiate logging
logging.basicConfig(
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	level=logging.INFO
)

# initiate the bot # pass tokens
bot = telebot.TeleBot(BOT_TOKEN)
print("TeleBot library connected.") # debugging print

# functions for commands
## start
@bot.message_handler(commands=['start'])
def start_command(message):
	'''greet the user at the start'''
	bot.send_message(message.chat.id, 'Hello! Nice to meet you. I am your personal assistant, Sannie!\n\nDo not hesitate to ask for help with "/help".')

## help
@bot.message_handler(commands=['help'])
def help_command(message):
	'''provide guidance'''
	bot.send_message(message.chat.id, 'This bot will get you current weather status based on your input. Try "/weather" or send me some common greetings.')

## pray
@bot.message_handler(commands=['pray'])
def pray_command(message):
	'''pray for Myanmar'''
	bot.send_message(message.chat.id, 'May Myanmar be at peace. May Myanmar prosper. Viva La Revolution!')

## weather
@bot.message_handler(commands=['weather'])
def weather_command(message):
	'''ask the user to enter a location (city) after the '/weather' command'''
	location = 'Enter a city:\nExample: yangon'
	sent_message = bot.send_message(message.chat.id, location, parse_mode='Markdown')
	bot.register_next_step_handler(sent_message, fetch_weather)
	return location



# functions for producing specific responses
def choose_response(text: str) -> str:
	processed_text: str = text.lower() # transform text into lowercase for word-processing

	for greetings in ['hello', 'hi', 'mingalarbar']:
		if greetings in processed_text:
			return 'Mingalarbar :)'

	if 'bot' in processed_text:
		return 'You are right. I am a bot.'

	if 'weather' in processed_text:
		return 'Do you mean "/weather"?'

	if 'myanmar' in processed_text:
		return 'Check out "/pray"'

	if 'sannie' in processed_text:
		return 'I am Sannie, your favorite personal assistant.'

	if 'thank' in processed_text:
		return 'I am greatful to help you.'

	for endings in ['bye', 'byebye', 'goodbye', 'tartar']:
		if endings in processed_text:
			return 'Bye! I hope we meet again.'

	return f'I do not understand your message, you said "{processed_text}"' # echo

# function to reply messages
@bot.message_handler(func=lambda msg: True)
def reply_message(message):
	'''echoes back any other messages bot receives from user'''
	text_to_reply = choose_response(message.text)
	bot.reply_to(message, text_to_reply)


## more functions for weather command
### function to handle locations
def location_handler(message):
	'''
	This function returns the latitude and longitude coordinated from user's input (location) using the Nominatim geocoder.
	>>>location is found - returns the rounded latitude and longitude
	>>>else - returns Location not found
	'''
	location = message.text
	# Create a geocoder instance
	geolocator = Nominatim(user_agent="my_app")

	try:
		# Get the latitude and longitude
		location_data = geolocator.geocode(location)
		latitude = round(location_data.latitude,2)
		longitude = round(location_data.longitude,2)
		# print(latitude, longitude)
		return latitude, longitude
	except AttributeError:
		print("Location not found.")



### function to connect weather website URL
def get_weather(latitude,longitude):
	'''
	arguments: latitude, longitude
	This function takes in arguments as inputs and constructs URL to make API call to OpenWeatherMap API.
	It returns a response JSON after fetching weather data for the specified latitude and longitude.
	'''
	url = f'https://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={WEATHER_TOKEN}'
	response = requests.get(url)
	# print(response.json())
	return response.json()



### function to get weather answer
def fetch_weather(message):
	'''
	This function gets called when the user provides location in response to the '/weather' command.
	It uses the 'get_location' function to get latitude & longitude of the provided location and 'get_weather' function to fetch the weather data
	extracts weather description from API response and sends to user as message.
	'''
	latitude, longitude = location_handler(message)
	weather = get_weather(latitude,longitude)
	data = weather['list']
	data_2 = data[0]
	info = data_2['weather']
	data_3 = info[0]
	description = data_3['description']
	weather_message = f'*Weather:* {description}\n'
	bot.reply_to(message, weather_message, parse_mode='Markdown')



# poll (check new messages) indefinitely
print('Polling process has begun...') # debugging print
bot.infinity_polling()
