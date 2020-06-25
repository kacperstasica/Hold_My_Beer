import os

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import EmailMessage, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, TemplateView, FormView

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, ContactForm


class UserCreateView(SuccessMessageMixin, CreateView):
    model = get_user_model()
    form_class = UserRegisterForm
    success_url = reverse_lazy(
        'users:login'
    )
    template_name = 'users/register.html'
    success_message = "%(username)s was created successfully. You are now able to log in!"


class ProfileView(LoginRequiredMixin, View):

    def get(self, request):
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        context = {
            'u_form': u_form,
            'p_form': p_form,
        }
        return render(request, 'users/profile.html', context)

    def post(self, request):
        u_form = UserUpdateForm(request.POST,
                                instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has ben updated!')
            return redirect('users:profile')


class ContactView(FormView):
    form_class = ContactForm
    template_name = 'users/contact_form.html'
    success_url = reverse_lazy('users:contact-success')

    def get_form_kwargs(self):
        kwargs = super(ContactView, self).get_form_kwargs()
        if self.request.user is not None:
            kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        subject = form.cleaned_data['subject']
        from_email = form.cleaned_data['from_email']
        message = form.cleaned_data['message']
        try:
            email = EmailMessage(
                subject,
                'from: {}\n {}'.format(from_email, message),
                from_email=from_email,
                reply_to=[from_email, ],
                to=[os.environ.get('EMAIL_USER')]
            )
            email.send()
            messages.success(self.request, 'Your message was sent. Thank you for contacting us!')
            return redirect('users:contact-success')
        except BadHeaderError:
            return HttpResponse('Invalid header found.')


class ContactSuccessView(TemplateView):
    template_name = 'users/contact_success.html'
