from django.contrib import admin

from .models import *

admin.site.register(Mail)
admin.site.register(MailBasicInfo)
admin.site.register(MailUserInfo)


