import datetime

from playhouse.signals import Model
from playhouse.postgres_ext import BigAutoField, CharField, IntegerField, DateTimeTZField


class Product(Model):
    id = BigAutoField(primary_key=True)
    name = CharField()
    count = IntegerField()
    blocked_count = IntegerField(default=0)
    created_at = DateTimeTZField(default=datetime.datetime.now())
    updated_at = DateTimeTZField(default=datetime.datetime.now())
