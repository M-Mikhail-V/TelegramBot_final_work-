1) Создать фаил .env
2) Прописать в нем токин своего бота:
    - BOT_TOKEN = "_____"
    Заполенить ID администратора:
    ADMINS = "______"
3) database.db можно удалить. При запуске первый раз БД создается автоматически, единственное будет необходимо заполнить название требуемых услуг вручную.
4) В папке .venv записана среда, можно не скачивать, но потребуется установка:
    aiogram==3.10.0
    peewee==3.17.6
    python-dotenv==1.0.1
    aiogram-dialog==2.2.0a5
    phonenumbers==8.13.40
