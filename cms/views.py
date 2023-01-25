from .models import *

import json
import re
from datetime import date, timedelta

from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.middleware.csrf import get_token
from django.forms.models import model_to_dict
from django.db.models.functions import TruncDay
from django.db.models import Count

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
        "archived": cfs.archived,
    }


def all_contact_form_submissions(request):
    cfs_objects = ContactFormSubmission.objects.all().order_by("date")
    all_cfs = {}
    for cfs in cfs_objects:
        all_cfs[cfs.id] = contact_form_submission_dict(cfs)
    return JsonResponse(all_cfs)


def get_subscribers(request):
    today = date.today()
    one_week_ago = today - timedelta(days=7)
    one_month_ago = today - timedelta(days=31)

    subscriber_objects = Contact.objects.filter(subscribed=True).order_by("added")
    all_time = subscriber_objects.count()
    this_week = subscriber_objects.filter(added__gte=one_week_ago).count()
    this_month = subscriber_objects.filter(added__gte=one_month_ago).count()

    subscribers = {
        "contacts": {},
        "added": {"allTime": all_time, "week": this_week, "month": this_month},
    }
    for s in subscriber_objects:
        subscribers["contacts"][s.id] = {
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
        return get_pageviews()


def get_pageviews_per_day(start_date):
    views_per_day_objects = (
        PageView.objects.annotate(day=TruncDay("date"))
        .filter(date__gte=start_date)
        .values("day")
        .annotate(c=Count("id"))
        .values("day", "c")
    )

    views_per_day = {}
    for d in views_per_day_objects:
        views_per_day[d["day"].strftime("%Y-%m-%d")] = d["c"]

    return views_per_day


def get_pageviews():
    today = date.today()
    one_week_ago = today - timedelta(days=7)
    one_month_ago = today - timedelta(days=31)

    views_per_day = get_pageviews_per_day(start_date=one_month_ago)

    return JsonResponse(
        {
            "totals": {
                "allTime": PageView.objects.count(),
                "week": PageView.objects.filter(date__gte=one_week_ago).count(),
                "month": PageView.objects.filter(date__gte=one_month_ago).count(),
            },
            "byDay": views_per_day,
        }
    )


# @csrf_exempt
# def upload_tm_image(request):
#     if request.method == "POST":
#         try:
#             # print(request.body

#             # )

#             some_bytes = request.body

#             # Open file in binary write mode
#             binary_file = open("my_file.png", "wb")

#             # Write bytes to file
#             binary_file.write(some_bytes)

#             # Close file
#             binary_file.close()

#             # storage_client = storage.Client.from_service_account_json(
#             #     "./cms/erudite-spot-374002-f32df51d5be4.json", project="win-together-ui"
#             # )
#             # bucket = storage_client.get_bucket("wtg-cms-images")
#             # path = "./cms/ test.txt"
#             # blob = bucket.blob("uploaded_test.txt")
#             # # blob.upload_from_filename(path)
#             return HttpResponse("image uploaded")
#         except Exception as e:
#             response = HttpResponse(f"something went wrong --> {e}")
#             response.status_code = 500
#             return response
#     else:
#         response = HttpResponse("must be a POST request")
#         response.status_code = 400
#         return response


@ensure_csrf_cookie
def set_csrf_token(request):
    # token = get_token(request)
    # print(token)
    return HttpResponse("token set")
