from django.db import models
from django.db.models import Model, CharField, TextField, DateTimeField, ImageField


# Create your models here.
class Post(Model):
    title = CharField(max_length=150)
    description = TextField(max_length=150)
    created_at = DateTimeField(auto_now_add=True)
    image = ImageField(upload_to='media/', null=True, blank=True)

    def __str__(self):
        return self.title
