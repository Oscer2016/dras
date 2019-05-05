from django.db import models
from mongoengine import *


connect('house', host='127.0.0.1', port=27017)

#class User(models.Model):
#    user_id = models.CharField(max_length=20)

class User(Document):
    username = StringField()
    password = StringField()

    meta = {'collection': 'user'}

#for i in User.objects[:]:
#    print i.username

