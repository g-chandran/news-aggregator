from django.urls import path
from .views import HomePageView, SignupView, aggregator, homeListView, HomeListView

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('signup/', SignupView.as_view(), name='signup'), 
    path('aggregator/', aggregator, name='aggregator'), 
]
