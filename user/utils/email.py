import uuid
import json

from django.core.cache import cache
from django.core.mail import send_mail


def validate_email(user, email):
    title = '验证你的电子邮箱 | conus 通知推送'
    body = '请打开下方连接以验证你的电子邮箱：\n'
    send_mail(title, body, None, email)
    cache.set(f'user:{user.pk}:validate_email', json.dumps({uuid.uuid4().hex: email}))
