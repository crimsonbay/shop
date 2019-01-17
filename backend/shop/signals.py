from django.db.models.signals import pre_save, post_delete, post_save
from django.dispatch import receiver
from .serializers import ProductIndexSerializer
from .models import Product, Order
from .es_client import es_client
from .models import UserProfile
from django.conf import settings
from .tasks import verify_user, email_order, new_email_order


# calls after new user created or updated
# if created NEW user then create user profile with uuid for user and call verify task for sending
# email with verification address
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance=None, created=False, **kwargs):
    if created:
        user_profile = UserProfile.objects.create(user=instance)
        verify_user.delay(user_profile.uuid, instance.email)


# calls after new product saved or updated
# save serialized product in Elasticsearch
@receiver(post_save, sender=Product, dispatch_uid="update_record")
def update_es_record(sender, instance, created=False, **kwargs):
    obj = ProductIndexSerializer(instance)
    obj.save(using=es_client)


# calls after product deleted
# delete serialized product from Elasticsearch
@receiver(post_delete, sender=Product, dispatch_uid="delete_record")
def delete_es_record(sender, instance, *args, **kwargs):
    obj = ProductIndexSerializer(instance)
    obj.delete(using=es_client, ignore=404)


# calls after order created or updated
# if NEW order created then calls email function for confirmation
@receiver(post_save, sender=Order)
def created_order(sender, instance, created=False, **kwargs):
    if created:
        new_email_order.delay(instance.uuid, instance.email, instance.status)


# calls before order save
# if this is NOT NEW order then if status changed it calls email task
# for inform customer about this
@receiver(pre_save, sender=Order)
def update_order(sender, instance, created=False, **kwargs):
    try:
        old_instance = Order.objects.get(id=instance.id)
    except:
        return
    if old_instance.status != instance.status:
        email_order.delay(instance.id, instance.email, instance.status)
