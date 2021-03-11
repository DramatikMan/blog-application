import smtplib
from email.mime.text import MIMEText

from celery import Celery


celery = Celery(
    'tasks',
    broker='amqp://guest:guest@localhost:5672',
    backend='rpc://'
    )


@celery.task
def log(msg):
    return msg


@celery.task(
    bind=True,
    ignore_result=True,
    default_retry_delay=300,
    max_retries=5
)
def remind(self, pk):
    reminder = Reminder.query.get(pk)
    msg = MIMEText(reminder.text)

    msg['Subject'] = 'Your reminder'
    msg['From'] = 'from@email.boop'
    msg['To'] = 'to@email.boop'

    try:
        smtp_server = smtplib.SMTP('localhost:1025')
        # smtp_server.starttls()
        # smtp_sever.login()
        smtp_server.sendmail(
            msg['From'],
            msg['To'],
            msg.as_string()
        )
        smtp_server.quit()
    except Exception as e:
        self.retry(exc=e)


def on_reminder_save(mapper, connect, self):
    remind.apply_async(args=(self.id,), eta=self.dt)
