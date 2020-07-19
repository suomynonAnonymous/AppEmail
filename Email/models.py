from django.contrib.auth.models import User
from django.db import models

LABEL_CHOICES = (('SP', 'Support'), ('AS', 'Assignment'), ('EX', 'Examination'),
                 ('PR', 'Practical'))


class Mail(models.Model):
    # sender_image = models.ImageField(upload_to="senders/", null=True)
    file_upload = models.FileField(upload_to="files/", blank=True, null=True)
    label = models.CharField(max_length=2, choices=LABEL_CHOICES, blank=True, null=True)
    subject = models.CharField(max_length=100, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    send_date = models.DateTimeField(auto_now_add=True)
    viewed_date = models.DateTimeField(auto_now=True)
    mail_send = models.BooleanField(default=False)
    mail_starred = models.BooleanField(default=False)
    mail_spam = models.BooleanField(default=False)
    mail_deleted = models.BooleanField(default=False)
    mail_viewed = models.BooleanField(default=False)
    mail_draft = models.BooleanField(default=False)

    # ## Relational Fields:
    sender = models.ForeignKey(User, on_delete=models.CASCADE,
                               blank=True, null=True,
                               related_name='%(class)s_requests_sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE,
                                 null=True, blank=True,
                                 related_name='%(class)s_requests_receiver')
    reply_parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE)

    # def spam_mail(self):
    #     self.mail_spam = True
    #     self.save()
    #
    # def star_mail(self):
    #     self.mail_starred = True
    #     self.save()

    # def deleted_mail(self):
    #     self.mail_deleted = True
    #     self.save()

    # def send_mail(self):
    #     self.mail_send = True
    #     self.save()

    # def viewed_mail(self):
    #     self.mail_viewed = True
    #     self.save()
    #
    # def unviewed_mail(self):
    #     self.mail_viewed = False
    #     self.save()

    def get_reply(self):
        return self.mail_set.all().order_by("-pk")

    def __str__(self):
        return self.subject
