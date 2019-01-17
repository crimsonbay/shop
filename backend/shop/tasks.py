from django.core.mail import send_mail
from .models import Order
from backend.celery import app
from backend.settings import SITE_ADDRESS


# Sending Email user verification
@app.task(name='shop.tasks.verify_user')
def verify_user(uuid, email):
    subject = 'Магазин. Подтвердите регистрацию'
    message = 'Вы получили это сообщение, т.к. зарегистрировались у нас. Подтвердите свою регисрацию,' \
              ' перейдя по ссылке' \
              + SITE_ADDRESS + '/api/verify-user?uuid={}'.format(uuid)
    mail_send = send_mail(subject, message, 'yobatestshop@gmail.com', [email, ])
    return mail_send


# Sending Email if order by status
@app.task(name='shop.tasks.email_order')
def email_order(order_id, email, status):
    if status == Order.REQUIRES_ATTENTION:
        subject = 'Магазин. Вы поздтвердили заказ'
        message = 'Вы подтвердили заказ в нашем магазине.'.format(order_id)
    elif status == Order.WORK_IN_PROGRESS:
        subject = 'Магазин. Заказ принят в работу'
        message = 'Заказ принят в работу. Номер заказа {}'.format(order_id)
    elif status == Order.COMPLETED:
        subject = 'Магазин. Заказ выполнен'
        message = 'Заказ выполнен. Номер заказа {}'.format(order_id)
    elif status == Order.REJECTED:
        subject = 'Магазин. Заказ отменен'
        message = 'Заказ отменен. Номер заказа {}'.format(order_id)
    mail_send = send_mail(subject, message, 'yobatestshop@gmail.com', [email, ])
    return mail_send


# Sending Email order verification
@app.task(name='shop.tasks.new_email_order')
def new_email_order(uuid, email, status):
    if status == Order.NOT_CONFIRMED:
        subject = 'Магазин. Вы сделали заказ'
        message = 'Подтвердите заказ по ссылке\n' \
                  + SITE_ADDRESS + '/verify-order?uuid={}'.format(uuid)
        try:
            mail_send = send_mail(subject, message, 'yobatestshop@gmail.com', [email, ])
            return mail_send
        except Exception as e:
            print(e)
            return
