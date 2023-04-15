from django.conf import settings
from django.core.mail import send_mail
from django.db import models


class EmailForContacts(models.Model):

    email = models.EmailField("E-mail менеджера")

    class Meta:
        verbose_name = 'E-mail'
        verbose_name_plural = 'E-mailы менеджеров'

    def sent_to(self, subject, tpl):
        return send_mail(from_email=settings.DEFAULT_FROM_EMAIL, message=tpl, subject=subject, recipient_list=[self.email])
