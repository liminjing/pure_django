from django.db import models

# Create your models here.
from mongoengine import *
from mongoengine import connect

connect('template',host='127.0.0.1',port=27017)

# ORM 对象关系映射(Object Relational Mapping)
class Pokemon(Document):
    #变量名需和列名完全一致
    name = StringField()
    types = ListField(StringField())
    rate = IntField()
    desc = StringField()
    meta = {'collection':'pokemon'}  #可不写，类名与集合名一样就行

# for i in Pokemon.objects:
#     print(i.name,i.types,i.rate,i.desc)



# for i in Pokemon.objects[:1]:   #用片分来获取对象——[:1]取一个对象数据
#     print(i)
#     print(i.name,i.types,i.rate,i.desc)
