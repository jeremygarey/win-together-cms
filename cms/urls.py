from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("team-members", views.all_team_members, name="all team members"),
    path("blog-posts", views.all_blog_posts, name="all blog posts"),
]
