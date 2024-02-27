from core.celery import celery_app

from utils.context_manager import SendEmailManager


@celery_app.task
def send_email_task(host,port, username, password, sender, recever, message):
    
    with SendEmailManager(host ,port) as mail:
        mail.login(username, password)
        mail.sendmail(sender, recever, message)

    return True


             