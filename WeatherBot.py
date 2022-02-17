import telebot
import requests

telegramToken = "5281039218:AAHxx1GOwasOUzsUVlRj-CKMn9AtIZqm2us"
weatherToken = "b05563abc9ede6e839bea4653076fcc4"

bot = telebot.TeleBot(telegramToken)


@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Hello, type a city and get a free forecast')

@bot.message_handler(content_types=["text"])
def handle_text(message):

    try:

        requestContent = requests.get("https://api.openweathermap.org/data/2.5/weather?q=" + message.text + "&appid=" + weatherToken)

        requestContent = requestContent.json()

        weatherDescr = requestContent['weather'][0]['description']

        tempKelvin = float(requestContent['main']['temp'])
        tempFeelLikeKelvin = float(requestContent['main']['feels_like'])

        tempCelsium = tempKelvin - 273.15
        tempFeelLikeCelsium = tempFeelLikeKelvin - 273.15

        humidity = float(requestContent['main']['humidity'])

        wind = float(requestContent['wind']['speed'])

        tempCelsium = round(tempCelsium,1)
        tempFeelLikeCelsium = round(tempFeelLikeCelsium,1)
        humidity = round(humidity,1)
        wind = round(wind,1)

        FullDescriptin = "Current weather state : " + weatherDescr + "\n"
        FullDescriptin += "temperature " + str(tempCelsium) + "C, feels like " + str(tempFeelLikeCelsium)  + "C" + "\n"
        FullDescriptin += "humidity " + str(humidity) + "%"  + "\n"
        FullDescriptin += "wind " + str(wind) + "m/s"

        bot.send_message(message.chat.id, FullDescriptin)

    except:
        bot.send_message(message.chat.id, "invalid request try again")

bot.polling(none_stop=True, interval=0)
