from peewee import SqliteDatabase, TextField, IntegerField, DateTimeField, Model, ForeignKeyField

db = SqliteDatabase('database.db')


class Users(Model):
    user_id = IntegerField()
    fullname = TextField()
    phone_number = TextField()

    class Meta:
        database = db


class Services(Model):
    name = TextField()

    class Meta:
        database = db


class Appointments(Model):
    user = ForeignKeyField(model=Users)
    service = ForeignKeyField(model=Services)
    date_time = DateTimeField()

    class Meta:
        database = db