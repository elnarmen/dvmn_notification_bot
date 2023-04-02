# dvmn_notification_bot
<b>Бот уведомляет о проверенных уроках на проекте Devman</b>

##  Установка
На вашем компьютере уже должен быть установлен Python3. Для загрузки проекта откройте терминал и перейдите в папку, в которую хотите загрузить файлы.

Затем введите команду:
```
git clone https://github.com/elnarmen/dvmn_notification_bot.git
```
## Настройка виртуального окружения
Создайте виртуальное окружение командой:
```
python3 -m venv venv
```
Активация виртуального окружения для Windows:

```
cd venv\Scripts
activate.bat
```

Для Linux:
```
source venv/bin/activate
```

## Установка зависимостей
Используйте pip для установки зависимостей:

   ```
   pip install -r requirements.txt
   ```
## Переменные окружения
В папке с проектом создайте файл **`.env`** для хранения переменных окружения

#### DVMN_TOKEN
* Скопируйте ваш токен на сайте [https://dvmn.org/api/docs/](https://dvmn.org/api/docs/)

#### TELEGRAM_BOT_TOKEN и LOGS_TELEGRAM_BOT_TOKEN

* Через поиск телеграм найдите бот @BotFather. 
* Отправьте /start для получения списока всех его команд.
* Выберите команду /newbot - бот попросит придумать имя вашему новому боту. 
Необходимо создать два бота - основной бот и бот, который будет получать сообщения о логах
* Сохраните полученные токены в переменных `TELEGRAM_BOT_TOKEN` и LOGS_TELEGRAM_BOT_TOKEN в файле `.env`:

```
TELEGRAM_TOKEN=<Токен для основного бота>

LOGS_TELEGRAM_BOT_TOKEN = <Токен для бота логов>

```

#### CHAT_ID

Чтобы получить свой chat_id, напишите в Telegram специальному боту: `@userinfobot`

Сохраните chat_id в переменной `CHAT_ID` в файле `.env`:
```
CHAT_ID=<Ваш chat_id>
```


## Запуск бота в Docker
Docker уже должен быть установлен на вашем сервере.
Инструкция по установке: [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)

Перейдите в папку с проектом и создайте образ с помощью команды:
```
docker build -t notification_bot .
```

Запустите Docker-контейнер:
```
docker run --env-file .env notification_bot
```

Чтобы контейнер продолжал работать после выхода из командной строки, добавьте флаг `-d` (daemon mode). 
Чтобы контейнер перезапускался при перезагрузке сервера, добавьте флаг `--restart alway`
