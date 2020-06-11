from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


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
