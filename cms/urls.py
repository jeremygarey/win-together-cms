from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("contact", views.handle_contact_form, name="handle contact form"),
    path(
        "contact-form-submissions",
        views.all_contact_form_submissions,
        name="all contact form submissions",
    ),
    path(
        "email-subscribe", views.handle_email_subscribe, name="handle email subscribe"
    ),
    path("team-members", views.all_team_members, name="all team members"),
    path("team-members/update", views.update_team_member, name="update team member"),
    path("team-members/<int:id>", views.get_team_member, name="get team member"),
    path("blog-posts", views.all_blog_posts, name="all blog posts"),
    path("blog-posts/update", views.update_blog_post, name="update blog post"),
    path("blog-posts/<int:id>", views.get_blog_post, name="get blog post"),
    path("pageviews", views.add_pageview, name="add pageview"),
    path("sign-in", views.sign_in, name="sign in"),
    path("subscribers", views.get_subscribers, name="get subscribers"),
    path("set-csrf-token", views.set_csrf_token, name="set csrf token"),
]
