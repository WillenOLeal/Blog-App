from django.dispatch import receiver
from django.db.models.signals import post_save
#from .models import CustomUser, Profile
from .models import CustomUser


# @receiver(post_save, sender=CustomUser)
# def create_profile_after_user_registration(sender, instance, created, **kwargs):
#     if created:
#         profile = Profile(user=instance)
#         profile.save()


# @receiver(post_save, sender=CustomUser)
# def save_profile_when_user_is_saved(sender, instance, **kwargs):
#     instance.profile.save()
