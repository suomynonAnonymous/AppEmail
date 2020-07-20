from django.forms import ModelForm

from Email.models import Mail


class MailForm(ModelForm):
    class Meta:
        model = Mail
        fields = "__all__"
