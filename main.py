import os
from dotenv import load_dotenv
import requests
import telegram


def send_message(bot, chat_id, lesson_title, is_negative_result, lesson_url):
    text = f'У вас проверили работу "{lesson_title}".'

    text += [
        '\nПреподователю все понравилось. Можно приступать к следущему уроку!',
        '\nК сожалению, в работе нашлись ошибки.',
        ][is_negative_result]

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
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        decoded_response = response.json()
        if decoded_response['status'] == 'timeout':
            params = {
                'timestamp': decoded_response['timestamp_to_request']
            }
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            decoded_response = response.json()
        if decoded_response['status'] == 'found':
            for attempt in decoded_response['new_attempts']:
                lesson_title = attempt['lesson_title']
                is_negative_result = attempt['is_negative']
                lesson_url = attempt['lesson_url']

                send_message(
                    bot, chat_id, lesson_title,
                    is_negative_result, lesson_url
                )


if __name__ == '__main__':
    try:
        main()
    except (requests.exceptions.ReadTimeout, ConnectionError):
        main()
