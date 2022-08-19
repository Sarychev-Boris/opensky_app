from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.views import logout_then_login
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views import generic
from django.shortcuts import render


def logout_view(request):
    a = logout_then_login
    context = {
        'exit': a
    }
    return render(request=request, template_name='/logout.html', context=context)


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'