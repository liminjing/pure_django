import os
from django.core.mail import send_mail,EmailMultiAlternatives

os.environ['DJANGO_SETTINGS_MODULE'] = 'pure_django.settings'


if __name__ == '__main__':

    #发送纯文本邮件
    """
        send_mail(
        '来自maggy的测试邮件', #邮件主题
        '欢迎访问localhost:8000.com', #邮件内容
        'maggy_li@163.com', #发送方
        ['114416663@qq.com',], #接收方
    )
    """

    #发送html邮件
    subject, from_email, to = '来自maggy_li的测试邮件', 'maggy_li@163.com', '114416663@qq.com' #text_content是当HTML内容无效时的替代txt文本
    text_content = '欢迎访问www.liujiangblog.com，这里是刘江的博客和教程站点，专注于Python和Django技术的分享！'
    html_content = '<p>欢迎访问<a href="http://www.liujiangblog.com" target=blank>www.liujiangblog.com</a>，这里是刘江的博客和教程站点，专注于Python和Django技术的分享！</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()