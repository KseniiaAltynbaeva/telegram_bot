import telegram
from telegram.ext import Updater, CommandHandler
import requests


def start(update, context):
    user = update.effective_user
    ans = "Hello, " + user.first_name + ", I'm a WeatherBot! \n Type /help to get further information."
    context.bot.send_message(chat_id=update.effective_chat.id, text=ans)


def get_help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="/weather <city> -  get current weather in chosen city \n"
                                  " /article - in order to get entertained you'll receive"
                                  " a random article from Wikipedia")


def get_article(update, context):
    url = 'https://en.wikipedia.org/w/api.php?format=json&action=query&generator=random&grnnamespace=0&grnlimit=1&prop=extracts&exintro&explaintext'
    response = requests.get(url)
    data = response.json()
    key = list(data['query']['pages'].keys())[0]
    title = data['query']['pages'][key]['title']
    extract = data['query']['pages'][key]['extract']
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='<b>' + title + '</b>' + '\n' + extract,
                             parse_mode=telegram.ParseMode.HTML)


def get_weather(update, context):
    city = ' '.join(context.args)
    weather_site = "https://api.openweathermap.org/data/2.5/weather?"
    api = 'a576f91ba3f1793731b8cb997d3b1bf8'
    url = weather_site + "q=" + city + "&appid=" + api + "&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        main = data['main']
        report = data['weather']
        temperature = str(main['temp']) + "℃"
        context.bot.send_message(chat_id=update.effective_chat.id, text='<b>' + city.capitalize() + '</b>' + '\n' + f"Temperature: {temperature}" +'\n'
                                 +f"Weather Report: {report[0]['description']}",
                             parse_mode=telegram.ParseMode.HTML)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="No such city.")


def main():

    updater = Updater(token='', use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", get_help))
    dispatcher.add_handler(CommandHandler("weather", get_weather))
    dispatcher.add_handler(CommandHandler("article", get_article))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
