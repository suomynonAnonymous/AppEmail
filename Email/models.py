from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone

LABEL_CHOICES = (('SP', 'Support'), ('AS', 'Assignment'), ('EX', 'Examination'),
                 ('PR', 'Practical'))


class Mail(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE,
                               blank=True, null=True,
                               related_name='%(class)s_requests_sender')
    # sender_image = models.ImageField(upload_to="senders/", null=True)
    file_upload = models.FileField(upload_to="files/", blank=True, null=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE,
                                 null=True, blank=True,
                                 related_name='%(class)s_requests_receiver')
    label = models.CharField(max_length=2, choices=LABEL_CHOICES, blank=True, null=True)
    subject = models.CharField(max_length=100, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    send_date = models.DateTimeField(auto_now=True)
    viewed_date = models.DateTimeField(auto_now=True)
    mail_send = models.BooleanField(default=False)
    starred = models.BooleanField(default=False)
    spam = models.BooleanField(default=False)
    mail_deleted = models.BooleanField(default=False)

    def spam_mail(self):
        self.spam = True
        self.save()

    def star_mail(self):
        self.starred = True
        self.save()

    def deleted_mail(self):
        self.mail_deleted = True
        self.save()

    def __str__(self):
        return self.subject
