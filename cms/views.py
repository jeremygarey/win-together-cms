from .models import *

from django.http import HttpResponse, JsonResponse

# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the Cms index.")


def all_team_members(request):
    tm_objects = TeamMember.objects.all()
    team_members = {}
    for tm in tm_objects:
        team_members[tm.id] = {
            "name": tm.name,
            "profileImage": tm.profile_image,
            "jobTitle": tm.job_title,
            "email": tm.email,
            "shortBio": tm.short_bio,
            "longBio": tm.long_bio,
        }
    return JsonResponse(team_members)


def all_blog_posts(request):
    bp_objects = BlogPost.objects.all()
    blog_posts = {}
    for bp in bp_objects:
        blog_posts[bp.id] = {
            "name": bp.name,
            "body": bp.body,
            "summary": bp.summary,
            "mainImage": bp.main_image,
            "thumbnailImage": bp.thumbnail_image,
            "updatedDate": bp.updated,
        }
    return JsonResponse(blog_posts)
