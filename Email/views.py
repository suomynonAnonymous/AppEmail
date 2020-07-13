from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import View, CreateView, UpdateView

from .forms import MailForm
from .models import Mail
from django.core.files.storage import FileSystemStorage


class EmailListView(View):
    view = {}

    def get(self, request):
        # self.view['mail'] = Mail.objects.all()
        self.view['mail'] = Mail.objects.filter(receiver=self.request.user)
        return render(self.request, 'Email/mail.html', self.view)


class SendEmailListView(View):
    view = {}

    def get(self, request):
        # self.view['mail'] = Mail.objects.all()
        self.view['mail'] = Mail.objects.filter(sender=self.request.user)
        return render(self.request, 'Email/mail.html', self.view)


class SearchView(View):
    view = {}

    def get(self, request):
        query = request.GET.get('query', None)
        if not query:
            return redirect('Email/mail.html')
        self.view['mail'] = Mail.objects.filter(
            receiver=self.request.user).filter(
            Q(sender__username__icontains=query) | Q(body__icontains=query) | Q(subject__icontains=query))
        return render(self.request, 'Email/mail.html', self.view)


def compose(request):
    if request.method == 'POST' and request.FILES['files']:
        # if request.method == 'POST':
        # print(request.POST)
        print(request.GET.get('draft', None))
        is_draft = request.GET.get('draft', None)
        to = request.POST['to']
        user_list_r = to.split(',')
        uor_list = []
        for u in user_list_r:
            if User.objects.filter(username__iexact=u).count() != 1:
                continue
            else:
                uor_list.append(User.objects.get(username__iexact=u))
        print("userlist", uor_list)
        # uor_list = [User.objects.get(username=x) for x in user_list_r]
        subject = request.POST.get('subject', "")
        if request.FILES.get('files', None):
            files = request.FILES['files']
            fs = FileSystemStorage()
            filename = fs.save(files.name, files)
            file_upload_url = fs.url(filename)
        body = request.POST.get('body', "")
        for u in uor_list:

            data = Mail()
            data.sender = request.user,
            if len(uor_list):
                data.receiver = u,
            data.subject = subject,
            if request.FILES.get('files', None):
                data.file_upload = file_upload_url,

            data.body = body
            data.save()

        #     data = Mail.objects.create(
        #         sender=request.user,
        #         receiver=u,
        #         subject=subject,
        #         file_upload=file_upload_url,
        #         body=body
        #     )
        #     data.save()
        #     print("saved")
        #
        # if len(uor_list) == 0:
        #     data = Mail.objects.create(
        #         sender=request.user,
        #         subject=subject,
        #         body=body
        #     )
        #     data.save()
        return redirect('/inbox')

    # return redirect('/inbox')
    # if data.is_valid:
    #     try:
    #         data.save()
    #         # messages.success(request, 'Email has been sent !')
    #         print('Email has been send')
    #         return redirect('/')
    #     except:
    #         pass
    # else:
    #     print("Email Cannot be Send")


# def inbox_counter(user):
#     return user.messages_set.filter(read=False).count()

class DraftEmail(UpdateView):
    model = Mail
    form_class = MailForm
    template_name = "Email/mail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['mail'] = Mail.objects.filter(receiver=self.request.user)
        return context
