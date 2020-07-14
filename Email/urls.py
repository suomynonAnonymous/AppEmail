from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import MailListView, MailCreateView, mail_spam, mail_starred, mail_deleted

urlpatterns = [
    path('mail_list_class', MailListView.as_view(), name='mail_list_class'),
    path('mail_create_class', MailCreateView.as_view(), name='mail_create_class'),
    path('mail_spam/<int:pk>', mail_spam, name='mail_spam'),
    path('mail_starred/<int:pk>', mail_starred, name='mail_starred'),
    path('mail_deleted/<int:pk>', mail_deleted, name='mail_deleted'),



    # path('search', SearchView.as_view(), name='search'),
    # path('inbox', EmailListView.as_view(), name='email_list'),
    # path('send', SendEmailListView.as_view(), name='send_list'),
    # path('compose', compose, name='compose'),
    # path('draft/<int:pk>', DraftEmail.as_view(), name='draft'),
    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)