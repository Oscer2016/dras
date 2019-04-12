from django.db import models

class Visualization(models.Model):
    region = models.CharField(max_length=20)

