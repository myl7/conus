from email.header import Header
from email.utils import parseaddr, formataddr
from email.mime.text import MIMEText
import smtplib
from typing import Optional

from celery import shared_task
from celery.signals import worker_process_init, worker_process_shutdown

from conus import settings

server: Optional[smtplib.SMTP] = None


@worker_process_init.connect
def connect_smtp_server(**kwargs):
    global server
    server = smtplib.SMTP(settings.EMAIL_SMTP_HOST, settings.EMAIL_SMTP_PORT)
    server.login(settings.EMAIL_SMTP_USERNAME, settings.EMAIL_SMTP_PASSWORD)
    server.starttls()


def _format_email_addr(addr, name):
    # Handle Chinese characters
    name, addr = parseaddr(f'{name} <{addr}>')
    return formataddr((Header(name, 'utf-8').encode(), addr))


@shared_task
def notify_email(accounts, title, body):
    email = MIMEText(body, 'plain', 'UTF-8')
    email['From'] = _format_email_addr(settings.EMAIL_FROM_ADDR, settings.EMAIL_FROM_NAME)
    email['To'] = ','.join([_format_email_addr(addr, name) for addr, name in accounts])
    email['Subject'] = f'{title if title else "无标题"} | conus 通知推送'
    server.sendmail(settings.EMAIL_FROM_ADDR, [addr for addr, _ in accounts], email.as_string())


@worker_process_shutdown.connect
def quit_smtp_server(**kwargs):
    global server
    server.quit()
