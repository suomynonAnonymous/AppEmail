from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, ListView

from .forms import MailForm
from .models import Mail


class MailListView(ListView):
    model = Mail
    paginate_by = 10
    template_name = "Email/mail.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.order_by('-send_date')
        queryset = queryset.filter(Q(receiver=self.request.user) | Q(sender=self.request.user))
        email_type = self.request.GET.get('email_type', "inbox")
        if email_type == "inbox":
            queryset = queryset.filter(receiver=self.request.user, mail_deleted=False, mail_spam=False,
                                       mail_draft=False)
        if email_type == "send":
            queryset = queryset.filter(sender=self.request.user, mail_send=True, mail_deleted=False)
        if email_type == "draft":
            queryset = queryset.filter(sender=self.request.user, mail_send=False, mail_deleted=False)
        if email_type == "starred":
            queryset = queryset.filter(mail_starred=True, mail_deleted=False)
        if email_type == "spam":
            queryset = queryset.filter(receiver=self.request.user, mail_spam=True, mail_deleted=False)
        if email_type == "trash":
            queryset = queryset.filter(mail_deleted=True)
        search = self.request.GET.get('search', "")
        queryset = queryset.filter(
            Q(sender__username__icontains=search) | Q(body__icontains=search) | Q(subject__icontains=search))
        filter_type = self.request.GET.get('filter', "")
        if filter_type == "date":
            queryset = queryset.order_by('-send_date')
        if filter_type == "from":
            queryset = queryset.order_by('-sender')
        if filter_type == "subject":
            queryset = queryset.order_by('subject')
        if filter_type == "size":
            queryset = queryset.order_by('')

        print(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['user_list'] = User.objects.all()
        context['email_type'] = self.request.GET.get('email_type', "inbox")
        context['inbox_count'] = Mail.objects.filter(receiver=self.request.user, mail_deleted=False, mail_spam=False,
                                                     mail_draft=False, mail_viewed=False).count()
        context['starred_count'] = Mail.objects.filter(mail_starred=True, mail_deleted=False).count()
        context['trash_count'] = Mail.objects.filter(mail_deleted=True).count()
        context['search_q'] = self.request.GET.get('search', '')
        return context


class MailCreateView(CreateView):
    model = Mail
    form_class = MailForm
    template_name = "Email/mail.html"
    success_url = reverse_lazy("mail_list_class")

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context

    def form_invalid(self, form):
        print('errors:', form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):
        email_type = self.request.GET.get("email_type", "inbox")
        self.success_url += "?email_type=" + email_type

        is_send = self.request.GET.get("is_send", None)
        is_draft = self.request.GET.get("draft", None)

        if form.is_valid:
            self.object = form.save(commit=False)
        if is_send:
            self.object.mail_send = True
        if is_draft:
            self.object.mail_draft = True

        to_return = super().form_valid(form)
        return to_return


class MailMultipleCreate(View):
    def post(self, request, *args, **kwargs):
        receiver_list = self.request.POST['receiver_list']
        print(receiver_list, type(receiver_list))
        r_list = []
        if len(receiver_list):
            r_list = receiver_list.split(',')

        is_send = self.request.GET.get("is_send", None)
        is_draft = self.request.GET.get("draft", None)

        for r in r_list:
            mail_form = MailForm(request.POST, request.FILES)
            mail_obj = mail_form.save(commit=False)
            if is_send:
                mail_obj.mail_send = True
            if is_draft:
                mail_obj.mail_draft = True
            receiver = User.objects.get(pk=int(r))
            mail_obj.receiver = receiver
            print(mail_obj.receiver, mail_obj.subject)
            mail_obj.save()

        email_type = self.request.GET.get("email_type", "inbox")
        return redirect(reverse('mail_list_class') + '?email_type' + email_type)


class MailReplyView(CreateView):
    model = Mail
    form_class = MailForm
    template_name = "Email/mail.html"
    success_url = reverse_lazy("mail_list_class")

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context

    def form_invalid(self, form):
        print('errors:', form.errors)
        return super().form_invalid(form)

    def form_valid(self, form, **kwargs):
        email_type = self.request.GET.get("email_type", "inbox")
        self.success_url += "?email_type=" + email_type

        if form.is_valid:
            self.object = form.save(commit=False)

        self.object.mail_send = True
        self.object.reply_parent = get_object_or_404(Mail, pk=self.kwargs['pk'])
        self.object.subject = "<re>:" + self.object.reply_parent.subject
        self.object.label = self.object.reply_parent.label
        self.object.sender = self.request.user
        self.object.receiver = self.object.reply_parent.sender

        to_return = super().form_valid(form)
        return to_return


def mail_spam(request, pk):
    print("spam request")
    mail = get_object_or_404(Mail, pk=pk)
    mail.spam_mail()
    print(mail.pk, mail.mail_spam)
    return redirect('mail_list_class')


def mail_starred(request, pk):
    mail = get_object_or_404(Mail, pk=pk)
    if mail.mail_starred:
        mail.mail_starred = False
    else:
        mail.mail_starred = True
    mail.save()
    email_type = request.GET.get('email_type', "")
    return redirect(reverse('mail_list_class') + '?email_type=' + email_type)


def mail_deleted(request, pk):
    mail = get_object_or_404(Mail, pk=pk)
    mail.deleted_mail()
    email_type = request.GET.get('email_type', "")
    return redirect(reverse('mail_list_class') + '?email_type=' + email_type)


# def mail_send(request, pk):
#     mail = get_object_or_404(Mail, pk=pk)
#     mail.send_mail()
#     return redirect('mail_list_class', pk=mail.pk)
#
#
def mail_viewed(request, pk):
    mail = get_object_or_404(Mail, pk=pk)
    mail.viewed_mail()
    email_type = request.GET.get('email_type', "")
    return redirect(reverse('mail_list_class') + '?email_type=' + email_type)


def mail_unread(request, pk):
    mail = get_object_or_404(Mail, pk=pk)
    mail.unviewed_mail()
    email_type = request.GET.get('email_type', "")
    return redirect(reverse('mail_list_class') + '?email_type=' + email_type)
