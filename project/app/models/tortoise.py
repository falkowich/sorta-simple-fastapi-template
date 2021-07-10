from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class User(models.Model):
    name = fields.TextField()
    url = fields.TextField()
    created_at = fields.DatetimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} {self.url}"


UserSchema = pydantic_model_creator(User)
