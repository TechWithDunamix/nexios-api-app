from tortoise.models import Model
from tortoise import fields as f 
from uuid import uuid4
class BaseModel(Model):
    id = f.UUIDField(pk=True, default=uuid4)
    created_at = f.DatetimeField(auto_now_add=True)
    updated_at = f.DatetimeField(auto_now=True)

    class Meta:
        abstract = True
        table = "base_model"