import peewee as peewee


database = peewee.SqliteDatabase('weather.db')


class Weather(peewee.Model):
    title = peewee.CharField()
    temp_min = peewee.CharField()
    temp_max = peewee.CharField()
    date = peewee.DateField()

    class Meta:
        database = database


Weather.create_table()
