import os
from dotenv import load_dotenv
import requests
import telegram


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
    bot = telegram.Bot(token=telegram_token)
    url = 'https://dvmn.org/api/long_polling/'
    params = {'timestamp': ''}
    headers = {'Authorization': f'Token {dvmn_token}'}
    while True:
        try:
            response = requests.get(url, params=params, headers=headers)
        except (requests.exceptions.ReadTimeout, ConnectionError):
            continue
        response.raise_for_status()
        review_information = response.json()
        params = {
            'timestamp': review_information['timestamp_to_request']
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
