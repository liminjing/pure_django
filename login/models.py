from django.db import models

# Create your models here.
"""
需要一张用户表User，在用户表里需要保存下面的信息：
用户名
密码
邮箱地址
性别
创建时间
"""
class User(models.Model):
    gender=(
        ('male','男'),('female','女')
    )

    name=models.CharField(max_length=128,unique=True)
    password=models.CharField(max_length=128)
    email=models.EmailField(unique=True)
    sex=models.CharField(max_length=32,default='男',choices=gender)
    c_time=models.DateTimeField(auto_now_add=True)

    #邮件确认注册
    has_confirmed=models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering=['-c_time']
        verbose_name='用户'
        verbose_name_plural='用户'


#邮件确认
class ConfirmString(models.Model):
    code=models.CharField(max_length=128)
    user=models.OneToOneField('User',on_delete=models.CASCADE) #键的模型对象同时删除！
    c_time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name+': '+self.code

    class Meta:
        ordering=['-c_time']
        verbose_name='确认码'
        verbose_name_plural='确认码'