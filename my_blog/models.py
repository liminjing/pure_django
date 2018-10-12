from django.db import models

# Create your models here.
from mongoengine import *
from mongoengine import connect

connect('ganji',host='127.0.0.1',port=27017)

class Item_detail(Document):
    title=StringField()
    look_time=StringField()
    price=FloatField()
    area=ListField(StringField())
    pub_date=DateTimeField()
    type=StringField()
    cat=StringField()
    url=StringField()
    sold_date=IntField()
    date=DateTimeField()


# for item in Item_detail.objects[:10]:
#     print(item.title,item.date)
