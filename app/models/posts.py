from .base import BaseModel
from tortoise import fields as f

class Post(BaseModel):
    title = f.CharField(max_length=255)
    content = f.TextField()
    author = f.ForeignKeyField("models.User", related_name="posts")