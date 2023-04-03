FROM python:3.10

COPY requirements.txt /opt/app/requirements.txt

WORKDIR /opt/app

RUN pip install -r requirements.txt

COPY . /opt/app


ENV DVMN_TOKEN=${DVMN_TOKEN}
ENV LOGS_TELEGRAM_BOT_TOKEN=${LOGS_TELEGRAM_BOT_TOKEN}
ENV TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
ENV CHAT_ID=${CHAT_ID}

CMD ["python", "main.py"]
