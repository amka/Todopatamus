import datetime

import nanoid
from peewee import Model, CharField, DateTimeField
from todopatamus.services.db import db_service


class BaseModel(Model):
    id = CharField(default=nanoid.generate, max_length=16)

    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField()
    synced_at = DateTimeField(null=True)

    class Meta:
        database = db_service.db  # Use proxy for our DB.
