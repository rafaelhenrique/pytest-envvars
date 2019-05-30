from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=128, help_text='Product name')
