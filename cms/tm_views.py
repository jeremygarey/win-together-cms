from .models import *

import json
import re

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt


def team_member_dict(tm):
    return {
        "name": tm.name,
        "profileImage": tm.profile_image,
        "jobTitle": tm.job_title,
        "email": tm.email,
        "shortBio": tm.short_bio,
        "longBio": tm.long_bio,
        "archived": tm.archived,
    }


def all_team_members(request):
    tm_objects = TeamMember.objects.all()
    team_members = {}
    for tm in tm_objects:
        team_members[tm.id] = team_member_dict(tm)
    return JsonResponse(team_members)


def camel_to_snake(name):
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


@csrf_exempt
def update_team_member(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            change_fields = body["tm"]
            tm = TeamMember.objects.get(id=body["id"])

            for field in change_fields:
                setattr(tm, camel_to_snake(field), change_fields[field])

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


@csrf_exempt
def create_team_member(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)["tm"]

            tm = TeamMember(
                name=body["name"],
                profile_image="https://picsum.photos/300/200",  # TODO fix
                job_title=body["jobTitle"],
                email=body["email"],
                short_bio=body["shortBio"],
                long_bio=body["longBio"],
                archived=body["archived"],
            )

            tm.save()

            return JsonResponse({"id": tm.id, "tm": team_member_dict(tm)})
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
