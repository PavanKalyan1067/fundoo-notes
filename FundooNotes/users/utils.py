from time import sleep
from celery import shared_task

from Fundoo import settings
from django.core.mail import send_mail
import smtplib
from django.core.mail import EmailMessage
import threading


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


@shared_task
def sleepy(duration):
    sleep(duration)
    return None


class Util:
    @staticmethod
    def send_email(data):
        server = smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT)
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        msg = f'''
        {data['email_subject']}

        {data['email_body']}
        '''
        server.sendmail(settings.EMAIL_HOST_USER, [data['to_email']], msg)
        subject = data['email_subject']
        message = data['email_body'],
        recipient_list = [data['to_email']]
        from_email = settings.EMAIL_HOST_USER
        send_mail(subject, message, recipient_list=recipient_list, from_email=from_email)

    @staticmethod
    @shared_task
    def django_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], from_email=data['from_email'],
            to=[data['to_email']])
        # server.quit()
        EmailThread(email).start()
