from random import Random

from users.models import EmailVerifyRecord
from django.core.mail import send_mail
from MxOnline import settings
import string

def send_register_email(email,type="register"):
    email_record= EmailVerifyRecord()
    code=random_str(16)
    email_record.code=code
    email_record.email=email
    email_record.send_type=type
    email_record.save();
    if type=="register":
        email_tiltle="暮雪在线网注册激活链接"
        email_body="请点击下面链接激活账户:http://127.0.0.1:8000/active/{0}".format(code)
        # 传入 主题 ,body,邮件发送人,邮件接收邮箱 list
        send_status=send_mail(subject=email_tiltle,message=email_body,from_email=settings.EMAIL_FROM,recipient_list=[email])
        if send_status:
            pass
    if type=="forget":
        email_tiltle="暮雪在线网密码重置链接"
        email_body="请点击下面链接重置密码:http://127.0.0.1:8000/reset/{0}".format(code)
        # 传入 主题 ,body,邮件发送人,邮件接收邮箱 list
        send_status=send_mail(subject=email_tiltle,message=email_body,from_email=settings.EMAIL_FROM,recipient_list=[email])
        if send_status:
            pass

def random_str(randomlength=8):
    str=""
    chars=string.ascii_letters+ string.digits
    length=len(chars)
    random=Random()
    for i in range(0,randomlength):
        str+=chars[random.randint(0,length)]
    return str