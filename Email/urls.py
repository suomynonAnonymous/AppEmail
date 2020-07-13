from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import EmailListView, SearchView, compose, SendEmailListView, DraftEmail

urlpatterns = [
    path('inbox', EmailListView.as_view(), name='email_list'),
    path('send', SendEmailListView.as_view(), name='send_list'),
    path('search', SearchView.as_view(), name='search'),
    path('compose', compose, name='compose'),
    path('draft/<int:pk>', DraftEmail.as_view(), name='draft'),
    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)