from django.urls import path
from .views import (HomePageView, SignupView, aggregator, HomeListView, SubscriptionListView, ProfileView)

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('signup/', SignupView.as_view(), name='signup'), 
    path('subscription/<str:name>', SubscriptionListView.as_view(), name='subscription'),
    path('aggregator/', aggregator, name='aggregator'), 
    path('profile/', ProfileView.as_view(), name='profile')
]
