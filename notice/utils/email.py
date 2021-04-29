from django.core.mail import send_mass_mail


def notify_email(users, notice):
    title = f'{notice.title if notice.title else "无标题"} | conus 通知推送'
    send_mass_mail([(title, notice.body, None, user) for user in users if user.contactinfo.email])
