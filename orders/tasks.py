# from django.core.mail import send_mail
# from celery import shared_task
# from django.conf import settings
# from .models import Order


# @shared_task
# def send_order_confirmation(order_id):
#     """
#     Simulate sending an order confirmation.
#     This runs asynchronously via Celery.
#     """
#     try:
#         order = Order.objects.get(id=order_id)
        
      
#         # Here you could replace print statements with real email sending
#         # Example:
#         send_mail(
#             subject=f"Order #{order.id} Confirmation",
#             message=f"Your order status: {order.status}",
#             from_email=settings.DEFAULT_FROM_EMAIL,
#             recipient_list=[settings.EMAIL_RECIEVER]
#         )

#         return True
#     except Order.DoesNotExist:
#         print(f"[Celery Task] Order with ID {order_id} does not exist")
#         return False


# # tasks.py
# from celery import shared_task
# from django.core.mail import send_mail
# from .models import Order
# from django.conf import settings

# @shared_task
# def send_order_confirmation(order_id):
#     order = Order.objects.get(id=order_id)
    
#     # Only queue sending email, don't do heavy prints in the API
#     send_mail(
#         subject=f"Order #{order.id} Confirmation",
#         message=f"Your order status: {order.status}",
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         recipient_list=[settings.EMAIL_RECIEVER],
#         fail_silently=True
#     )

from celery import shared_task
from django.core.mail import send_mail
from .models import Order
from django.conf import settings
from celery.exceptions import MaxRetriesExceededError

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_order_confirmation(self, order_id):
    try:
        order = Order.objects.get(id=order_id)
        send_mail(
            subject=f"Order #{order.id} Confirmation",
            message=f"Your order status: {order.status}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.EMAIL_RECIEVER],
            fail_silently=False  # raise exception if email fails
        )
    except Exception as e:
        print(f"[Celery Task] Error sending email for order {order_id}: {e}")
        try:
            self.retry(exc=e)  # retry the task automatically
        except MaxRetriesExceededError:
            print(f"[Celery Task] Max retries reached for order {order_id}")
