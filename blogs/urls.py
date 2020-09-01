from django.urls import path
from .views import (HomePageView, SignupView, aggregator, HomeListView, SubscriptionListView, profileView,
    addProfile,
    removeProfile,
)

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('signup/', SignupView.as_view(), name='signup'), 
    path('subscription/<str:name>', SubscriptionListView.as_view(), name='subscription'),
    path('aggregator/', aggregator, name='aggregator'), 
    path('profile/', profileView, name='profile'),
    path('add/<int:id>', addProfile, name='add-profile'),
    path('remove/<int:id>', removeProfile, name='remove-profile'),
]
