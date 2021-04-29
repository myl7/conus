import uuid
import json

from django.core.cache import cache
from django.core.mail import send_mail
from django.shortcuts import reverse
from django.conf import settings


def validate_email(user, email):
    title = '验证你的电子邮箱 | conus 通知推送'
    token = uuid.uuid4().hex
    body = (
        '请打开下方连接以验证你的电子邮箱：\n'
        f'{settings.EMAIL_SITE_URL}{reverse("user:validate_email")}?token={token}'
    )
    send_mail(title, body, None, [email])
    cache.set(f'user:{user.pk}:validate_email', json.dumps({token: email}))
