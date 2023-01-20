from .models import *

import json

from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.middleware.csrf import get_token
from django.forms.models import model_to_dict

from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie


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


@csrf_exempt
def update_team_member(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            change_fields = body["tm"]
            tm = TeamMember.objects.get(id=body["id"])

            for field in change_fields:
                setattr(tm, field, change_fields[field])

            tm.save()

            return JsonResponse(model_to_dict(tm), safe=False)
        except Exception as e:
            return HttpResponse(f"something went wrong --> {e}")
    else:
        return HttpResponse("must be a POST request")


def get_team_member(request, id):
    try:
        tm = TeamMember.objects.get(id=id)
        return JsonResponse(
            {
                "name": tm.name,
                "profileImage": tm.profile_image,
                "jobTitle": tm.job_title,
                "email": tm.email,
                "shortBio": tm.short_bio,
                "longBio": tm.long_bio,
            }
        )
    except Exception as e:
        return HttpResponse(f"something went wrong --> {e}")


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


@csrf_exempt
def update_blog_post(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            change_fields = body["bp"]
            bp = BlogPost.objects.get(id=body["id"])

            for field in change_fields:
                setattr(bp, field, change_fields[field])

            bp.save()

            return JsonResponse(model_to_dict(bp), safe=False)
        except Exception as e:
            return HttpResponse(f"something went wrong --> {e}")
    else:
        return HttpResponse("must be a POST request")


def get_blog_post(request, id):
    try:
        bp = BlogPost.objects.get(id=id)
        return JsonResponse(
            {
                "name": bp.name,
                "body": bp.body,
                "summary": bp.summary,
                "mainImage": bp.main_image,
                "thumbnailImage": bp.thumbnail_image,
                "updatedDate": bp.updated,
            }
        )
    except Exception as e:
        return HttpResponse(f"something went wrong --> {e}")


@csrf_exempt
def sign_in(request):
    body = json.loads(request.body)
    user = authenticate(request, username=body["email"], password=body["password"])

    if user is not None:
        login(request, user)
        return JsonResponse({"email": user.email})
    else:
        response = HttpResponse("Invalid credentials")
        response.status_code = 401
        return response


@ensure_csrf_cookie
def set_csrf_token(request):
    # token = get_token(request)
    # print(token)
    return HttpResponse("token set")
