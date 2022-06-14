from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from django.dispatch import receiver
from config import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User

from .models import Response, Post, Newsletter


@receiver(post_save, sender=Response)
def send_email_on_creation(sender, instance, created, **kwargs):
    if created:
        subject = 'New response'
        message = f'The user {instance.user} wrote a response to your post {instance.post.title}.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.post.user.email]

        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False,
        )
        print(f'Email sent to {instance.post.user.email}')

    if instance.status == True:
        subject = 'Response accepted'
        message = 'The author of the post accepted your review!'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.user.email]

        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False,
        )
        print(f'Email sent to {instance.user.email}')


@receiver(post_delete, sender=Response)
def send_email_on_deletion(sender, instance, **kwargs):
    subject = 'Response deleted'
    message = 'The author of the post deleted your review!'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [instance.user.email]

    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False,
    )


@receiver(post_save, sender=Newsletter)
def send_newsletter(sender, instance, created, **kwargs):
    users = User.objects.all()
    mail_list = [user.email for user in users]
    if created:
        subject = f'{instance.title}'
        message = f'{instance.text}'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = mail_list

        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False,
        )
        print(f'Newsletter sent to {mail_list}')
