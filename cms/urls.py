from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("contact", views.handle_contact_form, name="handle contact form"),
    path("team-members", views.all_team_members, name="all team members"),
    path("team-members/update", views.update_team_member, name="update team member"),
    path("team-members/<int:id>", views.get_team_member, name="get team member"),
    path("blog-posts", views.all_blog_posts, name="all blog posts"),
    path("blog-posts/update", views.update_blog_post, name="update blog post"),
    path("blog-posts/<int:id>", views.get_blog_post, name="get blog post"),
    path("sign-in", views.sign_in, name="sign in"),
    path("set-csrf-token", views.set_csrf_token, name="set csrf token"),
]
