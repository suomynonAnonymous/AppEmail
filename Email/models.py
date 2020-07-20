from django.contrib.auth.models import User
from django.db import models

LABEL_CHOICES = (('SP', 'Support'), ('AS', 'Assignment'), ('EX', 'Examination'),
                 ('PR', 'Practical'))


class Mail(models.Model):
    # sender_image = models.ImageField(upload_to="senders/", null=True)
    receivers = models.CharField(max_length=200, blank=True, null=True)
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
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              blank=True, null=True,
                              related_name='owners')
    related_mail = models.ForeignKey("self", blank=True, null=True,
                                        related_name='related_mails',
                                        on_delete=models.DO_NOTHING)

    def get_reply(self):
        # return self.mail_set.filter(receiver__isnull=True).order_by("-pk")
        return self.mail_set.filter().order_by("-pk")

    def get_receivers(self):
        r_list = []
        if self.receivers:
            if len(self.receivers):
                r_list = self.receivers.split(',')
            return [User.objects.get(pk=int(r)) for r in r_list]
        else:
            return []

    def get_receivers_display(self):
        r_list = self.get_receivers()
        return ' | '.join([x.username for x in r_list])

    def get_related_mails(self):
        # ## for reply:
        # return self.reply_parent.mail_set.filter(receiver__isnull=True).order_by("-pk")
        return self.reply_parent.mail_set.filter().order_by("-pk")

    def get_other_link(self):
        if self.reply_parent is None:
            return self.mail_set.all().order_by("pk")
        else:
            qs = self.reply_parent.mail_set.exclude(pk=self.pk) | Mail.objects.filter(pk=self.reply_parent.pk)
            return qs.order_by("pk")

    def __str__(self):
        return self.subject + "---" + self.owner.username
