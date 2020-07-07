# from django.db.models.signals import post_save
# from django.dispatch import receiver

# from profiles.models import Profile

# from .models import User

# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
# from django.urls import reverse

# from django_rest_passwordreset.signals import reset_password_token_created


# @receiver(post_save, sender=User)
# def create_related_profile(sender, instance, created, *args, **kwargs):

#     if instance and created:
#         instance.profile = Profile.objects.create(user=instance)





