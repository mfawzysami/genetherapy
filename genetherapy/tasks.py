from genetherapy import job
from django.core.mail import send_mail as email_now
from utils.logs import log
from django.conf import settings



@job.task(bind=True)
def send_email_msg(self, subject, message, recipient_list, html_message=True):
    try:
        if html_message:
            email_now(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list, fail_silently=False,
                      html_message=message)
        else:
            email_now(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list, fail_silently=False)

        log.info("Email Was Sent to : {0} , Subject: {1}".format(recipient_list, subject))
    except Exception as e:
        self.retry(e, countdown=3, max_retries=3)
        log.error(e.message)


@job.task
def SayHello():
    log.info("Saying Hello From a periodic task")