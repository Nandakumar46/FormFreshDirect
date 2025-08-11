# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import SignUpForm

# Use a class-based view for simplicity
class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('store:product_list') # Redirect after successful signup

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)