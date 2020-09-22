from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import Profile

from .models import User

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse

from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail 







# @receiver(post_save, sender=User)
# def create_related_profile(sender, instance, created, *args, **kwargs):

#     if instance and created:
#         instance.profile = Profile.objects.create(user_info=instance)

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    context = {
        #'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        #'email': reset_password_token.user.email,
        #'reset_password_url': "{}?token={}".format(reverse('password_reset/confirm/'), reset_password_token.key)
        'token': 'here is your token ' + reset_password_token.key
    }

    # render email text
    email_html_message = render_to_string('passmanager/user_reset_password.html', context)
    email_plaintext_message = render_to_string('passmanager/user_reset_password.txt', context)

    print('yes its working')
    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="fleeks"),
        # message:
        email_plaintext_message,
        # from:
        "mosesmvp@gmail.com",
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()



