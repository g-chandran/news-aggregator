from django.urls import path
from .views import HomePageView, SignupView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('signup/', SignupView.as_view(), name='signup'),  
]
