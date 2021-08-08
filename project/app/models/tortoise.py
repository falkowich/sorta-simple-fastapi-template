from enum import unique
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class User(models.Model):
    username = fields.CharField(max_length=255, unique=True)
    email = fields.TextField()
    full_name = fields.TextField()
    disabled = fields.BooleanField()
    hashed_password = fields.TextField()
    created_at = fields.DatetimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} {self.disabled}"


UserSchema = pydantic_model_creator(User)
