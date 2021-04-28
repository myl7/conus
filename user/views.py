import uuid
import re
from urllib.parse import urlencode
from xml.etree import ElementTree

from django.shortcuts import redirect, reverse
from django.conf import settings
from django.http.response import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
import requests

from .models import UstcCasCredential


def login_view(request):
    if request.user.is_anonymous:
        url = settings.USTC_CAS_LOGIN_URL + '?' + urlencode({
            'service': settings.USTC_CAS_CALLBACK_URL
        })
        return redirect(url)
    else:
        return redirect(reverse('notice:list_recv'))


def _validate_ticket(ticket):
    url = settings.USTC_CAS_VALIDATE_URL + '?' + urlencode({
        'service': settings.USTC_CAS_CALLBACK_URL,
        'ticket': ticket
    })
    response = requests.get(url)
    tree = ElementTree.fromstring(response.content.decode())[0]
    cas_tag = '{http://www.yale.edu/tp/cas}'
    if tree.tag != f'{cas_tag}authenticationSuccess':
        return None
    gid = tree.find('attributes').find(f'{cas_tag}gid').text.strip()
    uid = tree.find(f'{cas_tag}user').text.strip()
    return gid, uid


def validate_view(request):
    error = '登录失败，请重试'
    ticket = request.GET.get('ticket', None)
    if not ticket:
        return HttpResponse(error, status=401)
    res = _validate_ticket(ticket)
    if not res:
        return HttpResponse(error, status=401)
    gid, uid = res
    try:
        user = User.objects.get(username=uid)
    except User.DoesNotExist:
        user = User.objects.create_user(username=uid, password=uuid.uuid4().hex, first_name=uid)
        UstcCasCredential.objects.create(user=user, gid=gid)
        if not re.match(r'^[A-Z]{2}[0-9]{8}$', uid):
            user.user_permissions.add('notice.add_notice')
    login(request, user)
    return redirect(reverse('notice:list_recv'))


def logout_view(request):
    logout(request)
    return redirect(settings.USTC_CAS_LOGOUT_URL)
