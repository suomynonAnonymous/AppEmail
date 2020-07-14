from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView

from .forms import MailForm
from .models import Mail


class MailListView(ListView):
    model = Mail
    template_name = "Email/mail.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        email_type = self.request.GET.get('email_type', "inbox")
        if email_type == "inbox":
            queryset = queryset.filter(receiver=self.request.user)
        if email_type == "send":
            queryset = queryset.filter(sender=self.request.user)
        if email_type == "draft":
            queryset = queryset.filter(sender=self.request.user)
        if email_type == "starred":
            queryset = queryset.filter(sender=self.request.user)
        if email_type == "spam":
            queryset = queryset.filter(sender=self.request.user)
        if email_type == "trash":
            queryset = queryset.filter(sender=self.request.user)
        search = self.request.GET.get('search', "")
        queryset = queryset.filter(
            Q(sender__username__icontains=search) | Q(body__icontains=search) | Q(subject__icontains=search))
        print(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['user_list'] = User.objects.all()
        context['email_type'] = self.request.GET.get('email_type', "inbox")
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
        to_return = super().form_valid(form)
        return to_return


def mail_spam(request, pk):
    mail = get_object_or_404(Mail, pk=pk)
    mail.spam_mail()
    return redirect('mail_list_class', pk=pk)


def mail_starred(request, pk):
    mail = get_object_or_404(Mail, pk=pk)
    mail.star_mail()
    return redirect('mail_list_class', pk=pk)


def mail_deleted(request, pk):
    mail = get_object_or_404(Mail, pk=pk)
    mail.deleted_mail()
    return redirect('mail_list_class', pk=pk)
