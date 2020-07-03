from datetime import date, timedelta, datetime
from django.contrib import messages
from background_task import background
from django.conf import settings
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.utils import timezone


def add_message(request, message, tag='info'):
    request.session.setdefault('messages', {})[tag] = message


@background(schedule=0)
def send_delayed_email(to, sender, subject, message_template):
    print('Sending email to {}'.format(to))
    send_mail(
        subject = subject,
        html_message = message_template,
        message = strip_tags(message_template),
        from_email = sender,
        recipient_list = [to],
        fail_silently = False
    )
