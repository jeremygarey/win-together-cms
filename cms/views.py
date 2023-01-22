from .models import *

import json

from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.middleware.csrf import get_token
from django.forms.models import model_to_dict

from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie


def index(request):
    return HttpResponse("Hello, world. You're at the Cms index.")


@csrf_exempt
def handle_contact_form(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)

            try:
                contact = Contact.objects.get(email=body["email"])
            except Contact.DoesNotExist:
                contact = None
            if contact:
                # update first and last name info
                if body.get("firstName"):
                    contact.first_name = body["firstName"]
                if body.get("lastName"):
                    contact.last_name = body["lastName"]
                if body.get("subscribed"):
                    contact.subscribed = body["subscribed"]
                contact.save()

            else:
                # create new contact
                contact = Contact(
                    first_name=(body["firstName"] if body.get("firstName") else ""),
                    last_name=(body["lastName"] if body.get("lastName") else ""),
                    email=body["email"],
                    subscribed=(
                        body["subscribed"] if body.get("subscribed") else False
                    ),
                )
                contact.save()

            new_form_submission = ContactFormSubmission(
                contact=contact,
                message=body["message"],
            )
            new_form_submission.save()

            return HttpResponse("Contact form saved")
        except Exception as e:
            response = HttpResponse(f"something went wrong --> {e}")
            response.status_code = 500
            return response

    else:
        response = HttpResponse("must be a POST request")
        response.status_code = 400
        return response


def contact_form_submission_dict(cfs):
    return {
        "name": f"{cfs.contact.first_name} {cfs.contact.last_name}",
        "email": cfs.contact.email,
        "subscribed": cfs.contact.subscribed,
        "message": cfs.message,
        "date": cfs.date,
    }


def all_contact_form_submissions(request):
    cfs_objects = ContactFormSubmission.objects.all()
    all_cfs = {}
    for cfs in cfs_objects:
        all_cfs[cfs.id] = contact_form_submission_dict(cfs)
    return JsonResponse(all_cfs)


def get_subscribers(request):
    subscriber_objects = Contact.objects.filter(subscribed=True)
    subscribers = {}
    for s in subscriber_objects:
        subscribers[s.id] = {
            "email": s.email,
            "name": f"{s.first_name} {s.last_name}" if s.first_name else None,
            "date": s.added,
        }
    return JsonResponse(subscribers)


@csrf_exempt
def handle_email_subscribe(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)

            try:
                contact = Contact.objects.get(email=body["email"])
            except Contact.DoesNotExist:
                contact = None

            if contact:
                contact.subscribed = True
                contact.save()
            else:
                contact = Contact(email=body["email"], subscribed=True)
                contact.save()

            return HttpResponse("Successfully subscribed.")

        except Exception as e:
            response = HttpResponse(f"something went wrong --> {e}")
            response.status_code = 500
            return response
    else:
        response = HttpResponse("must be a POST request")
        response.status_code = 400
        return response


def team_member_dict(tm):
    return {
        "name": tm.name,
        "profileImage": tm.profile_image,
        "jobTitle": tm.job_title,
        "email": tm.email,
        "shortBio": tm.short_bio,
        "longBio": tm.long_bio,
    }


def all_team_members(request):
    tm_objects = TeamMember.objects.all()
    team_members = {}
    for tm in tm_objects:
        team_members[tm.id] = team_member_dict(tm)
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

            return JsonResponse(team_member_dict(tm))
        except Exception as e:
            response = HttpResponse(f"something went wrong --> {e}")
            response.status_code = 500
            return response
    else:
        response = HttpResponse("must be a POST request")
        response.status_code = 400
        return response


def get_team_member(request, id):
    try:
        tm = TeamMember.objects.get(id=id)
        return JsonResponse(team_member_dict(tm))
    except Exception as e:
        response = HttpResponse(f"something went wrong --> {e}")
        response.status_code = 500
        return response


def blog_post_dict(bp):
    return {
        "name": bp.name,
        "body": bp.body,
        "summary": bp.summary,
        "mainImage": bp.main_image,
        "thumbnailImage": bp.thumbnail_image,
        "updatedDate": bp.updated,
    }


def all_blog_posts(request):
    bp_objects = BlogPost.objects.all()
    blog_posts = {}
    for bp in bp_objects:
        blog_posts[bp.id] = blog_post_dict(bp)
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

            return JsonResponse(blog_post_dict(bp))
        except Exception as e:
            response = HttpResponse(f"something went wrong --> {e}")
            response.status_code = 500
            return response
    else:
        response = HttpResponse("must be a POST request")
        response.status_code = 400
        return response


def get_blog_post(request, id):
    try:
        bp = BlogPost.objects.get(id=id)
        return JsonResponse(blog_post_dict(bp))
    except Exception as e:
        response = HttpResponse(f"something went wrong --> {e}")
        response.status_code = 500
        return response


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


@csrf_exempt
def add_pageview(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            page_view = PageView(
                page_source=body["pageSource"],
                screen_height=int(body["screenHeight"]),
                screen_width=int(body["screenWidth"]),
                browser_type=body["browserType"],
                language=body["language"],
                time_zone=body["timeZone"],
            )
            page_view.save()
            return HttpResponse("added")
        except Exception as e:
            response = HttpResponse(f"something went wrong --> {e}")
            response.status_code = 500
            return response
    else:
        response = HttpResponse("must be a POST request")
        response.status_code = 400
        return response


@ensure_csrf_cookie
def set_csrf_token(request):
    # token = get_token(request)
    # print(token)
    return HttpResponse("token set")
