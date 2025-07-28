from django.urls import path

from tree_menu.views import (AboutView, ContactView, HomeView, ParentChildView,
                             ParentView, TeamView)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("team/", TeamView.as_view(), name="team"),
    path("contact/", ContactView.as_view(), name="contact"),
    path('parent/', ParentView.as_view(), name='parent'),
    path('parent/child/', ParentChildView.as_view(), name='parent_child'),
]

