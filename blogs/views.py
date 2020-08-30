from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic 

class HomePageView(TemplateView):
  template_name = "home.html"

class SignupView(generic.CreateView):
  form_class = UserCreationForm
  success_url = reverse_lazy('home')
  template_name = 'signup.html'