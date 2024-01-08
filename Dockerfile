FROM python:3.11-alpine

WORKDIR /app/molecule-tg-bot
COPY . .
RUN pip install -r requirements.txt
CMD ["sh", "start.sh"]