from django.forms import ModelForm

from Email.models import Mail, MailBasicInfo, MailUserInfo


class MailForm(ModelForm):
    class Meta:
        model = Mail
        fields = "__all__"


class MailBasicInfoForm(ModelForm):
    class Meta:
        model = MailBasicInfo
        fields = "__all__"


class MailUserInfoForm(ModelForm):
    class Meta:
        model = MailUserInfo
        fields = "__all__"


class MailUserInfoUpdateForm(ModelForm):
    class Meta:
        model = MailUserInfo
        fields = ["mail_type", "mail_starred", "mail_viewed"]