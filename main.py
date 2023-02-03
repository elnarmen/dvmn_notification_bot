import os
import time
import logging
from dotenv import load_dotenv
import requests
import telegram


class TelegramLogsHandler(logging.Handler):
    def __init__(self, bot, chat_id):
        super().__init__()
        self.bot = bot
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)


def send_message(bot, chat_id, lesson_title, is_negative_result, lesson_url):
    text = f'У вас проверили работу "{lesson_title}".'

    if is_negative_result:
        text += '\nК сожалению, в работе нашлись ошибки.'
    else:
        text += '\nПреподователю все понравилось. Можно приступать к следущему уроку!'

    text += f'\nСсылка на урок: {lesson_url}'

    bot.send_message(
        chat_id=chat_id,
        text=text
    )


def main():
    load_dotenv()

    dvmn_token = os.getenv('DVMN_TOKEN')
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('CHAT_ID')

    url = 'https://dvmn.org/api/long_polling/'
    params = {'timestamp': ''}
    headers = {'Authorization': f'Token {dvmn_token}'}
    waiting_time = 30

    bot = telegram.Bot(token=telegram_token)

    logger = logging.getLogger("bot_logger")
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(bot, chat_id))
    logger.info("Бот запущен")

    while True:
        try:
            response = requests.get(url, params=params, headers=headers)
            waiting_time = 30 # время ожидания в секундах перед запросом в случае проблем с сетью
        except requests.exceptions.ReadTimeout:
            continue
        except ConnectionError as err:
            logger.error(err)
            time.sleep(waiting_time)
            if waiting_time < 7200:
                waiting_time *= 1.2
                # время ожидания перед каждым последующим запросом будет
                # увеличивается на 20%, пока не достигнет 2 часов
            continue
        response.raise_for_status()
        review_information = response.json()
        params = {
            'timestamp': review_information.get('timestamp_to_request', '')
        }
        if review_information['status'] == 'found':
            for attempt in review_information['new_attempts']:
                lesson_title = attempt['lesson_title']
                is_negative_result = attempt['is_negative']
                lesson_url = attempt['lesson_url']

                send_message(
                    bot, chat_id, lesson_title,
                    is_negative_result, lesson_url
                )


if __name__ == '__main__':
    main()