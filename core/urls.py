from django.urls import path
from .views import (
    HomeView,
    SubscriberDetailView,
    SubscribersListView,
    SubscriberSearchView,
    AboutView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("subs", SubscribersListView.as_view(), name="subs"),
    path("search", SubscriberSearchView.as_view(), name="search"),
    path(
        "subs/<str:username>", SubscriberDetailView.as_view(), name="details"
    ),
    path("about", AboutView.as_view(), name="about"),
]
