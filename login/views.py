from django.shortcuts import render,redirect
from . import models
from . import form

# Create your views here.

def index(request):
    return render(request,'login/index.html')


#纯手工html编写表单元素
"""""
def login(request):
    if request.method=='POST':
        username=request.POST.get('username',None)
        password=request.POST.get('password',None)
        print(username,password)
        message='所有字段必须填写！'
        if username and password:# 确保用户名和密码都不为空
            username=username.strip()
            # 用户名字符合法性验证
            # 密码长度验证
            # 更多的其它验证.....

            try:
                user = models.User.objects.get(name=username)
                if user.password==password:
                    return redirect('/index/')
                else:
                    message='密码错误！'
            except:
                message='用户不存在！'
        return render(request,'login/login.html',{'message':message})
    return render(request,'login/login.html')
"""""
#表单方法验证
def login(request):
    if request.method=='POST':
        user_form=form.UserForm(request.POST)
        message='请检查填写内容！'
        if user_form.is_valid():
            username=user_form.cleaned_data['username']
            password=user_form.cleaned_data['password']
            print(username,password)

            try:
                user=models.User.objects.get(name=username)

                #是否已确认邮件注册
                if not user.has_confirmed:
                    message='请先前往邮箱确认，完成注册！'
                    return render(request,'login/login.html',locals())

                if user.password==hash_code(password): #加密

                    #使用sesseion
                    request.session['is_login']=True
                    request.session['user_id']=user.id
                    request.session['user_name']=user.name

                    return redirect('/index/')
                else:
                    message='密码错误！'
            except:
                message='用户不存在！'

        return render(request,'login/login.html',locals()) #locals()返回当前所有的本地变量字典

    user_form=form.UserForm()
    return render(request,'login/login.html',locals())


def logout(request):
    #未登陆状态
    if not request.session.get('is_login',None):
        return redirect('/index/')

    #登陆状态
    request.session.flush()
    #或者
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect('/index/')



def register(request):
    if request.method=='POST':
        reg_form=form.RegisterForm(request.POST)
        message='请检查填写内容！'
        if reg_form.is_valid():
            #获取数据
            password1=reg_form.cleaned_data['password1']
            password2=reg_form.cleaned_data['password2']

            #判断两次密码是否相同
            if password1!=password2:
                message='两次密码输入不一致！'
                return render(request, 'login/register.html', locals())

            else:
                # 判断用户是否唯一
                username=reg_form.cleaned_data['username']
                filter_user=models.User.objects.filter(name=username)
                if filter_user:
                    message='该用户名已存在！'
                    return render(request, 'login/register.html', locals())

                #判断邮箱是否唯一
                email=reg_form.cleaned_data['email']
                filter_email=models.User.objects.filter(email=email)
                if filter_email:
                    message='该邮箱已存在！'
                    return render(request, 'login/register.html', locals())

                user=models.User()
                user.name=username
                user.email=email
               #user.password=password1
                user.password=hash_code(password1) #密码加密
                user.sex=reg_form.cleaned_data['sex']
                user.save()

                #发送注册确认邮件
                code=make_confirm_string(user)
                send_email(email,code)
                message='邮件已发送，请前往邮箱确认注册！'
                return render(request, 'login/confirm.html', locals())  # 跳转到等待邮件确认页面，无需注册url

            #创建用户
    reg_form=form.RegisterForm()
    return render(request,'login/register.html',locals())


#hashcode编码
import hashlib
from datetime import datetime,timedelta

def hash_code(s, salt='mysite'):# 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


#生成邮件确认码
def make_confirm_string(user):
    now=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    code=hash_code(user.name,now) #以用户名为基础，now为‘盐’
    models.ConfirmString.objects.create(user=user,code=code)
    return code

from django.core.mail import EmailMultiAlternatives
from pure_django import settings

def send_email(send_to,code):
    subject = '来自maggy的注册确认邮件'

    text_content = '''感谢注册http://127.0.0.1:8000/，这里是刘江的博客和教程站点，专注于Python和Django技术的分享！\
                        如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

    html_content = '''
                        <p>感谢注册!</p>
                        <p>请点击<a href="http://{}/confirm/?code={}" target=blank>这里</a>完成注册确认！</p>
                        <p>此链接有效期为{}天！</p>
                        '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [send_to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


from django.utils import timezone
def user_confirm(request):
    code=request.GET.get('code',None)
    message=''
    try:
        confirm=models.ConfirmString.objects.get(code=code)
    except:
        message='无效的链接！'
        return render(request,'login/confirm.html',locals())


    now=timezone.now()
    ctime=confirm.c_time + timedelta(settings.CONFIRM_DAYS)
    if now>ctime:
        # can't compare offset-naive and offset-aware datetimes
        # 起因：正常的dateime.now() 得到的日期不能和Django数据库里面存储的日期数据做对比，两个解决办法：
        # 1、是把Django配置里面的USE_TZ设置成False，这样Django的数据就没有时区信息了。
        # 2、是在这个对比情景下，不要用datetime.now()来得当前数据，用以下代码：
        # from django.utils import timezone
        # now = timezone.now()

        message='您的邮件已过期，请重新注册！'
        confirm.user.delete() #删除过期用户
        return render(request,'login/confirm.html',locals())

    else:
        confirm.user.has_confirmed=True
        confirm.user.save()
        confirm.delete()
        message='注册确认成功，请登陆！'
        return render(request,'login/confirm.html',locals())