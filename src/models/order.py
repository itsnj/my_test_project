import datetime

from playhouse.signals import Model
from playhouse.postgres_ext import BigAutoField, CharField, IntegerField, ArrayField, DateTimeTZField
from src.enums.order_status import OrderStatus

order_status = [status.value for status in OrderStatus]


class Order(Model):
    id = BigAutoField(primary_key=True)
    product_ids = ArrayField(BigAutoField)
    quantity_ordered = ArrayField(IntegerField)
    status = CharField(choices=order_status)
    created_at = DateTimeTZField(default=datetime.datetime.now())
    updated_at = DateTimeTZField(default=datetime.datetime.now())
