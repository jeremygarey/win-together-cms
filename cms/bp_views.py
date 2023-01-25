from .models import *

import json
import re

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt


def camel_to_snake(name):
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def blog_post_dict(bp):
    return {
        "name": bp.name,
        "body": bp.body,
        "summary": bp.summary,
        "mainImage": bp.main_image,
        "thumbnailImage": bp.thumbnail_image,
        "updatedDate": bp.updated,
        "archived": bp.archived,
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
                setattr(bp, camel_to_snake(field), change_fields[field])

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


@csrf_exempt
def create_blog_post(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)["bp"]
            print(body)

            bp = BlogPost(
                name=body["name"],
                main_image="https://picsum.photos/300/200",  # TODO fix
                thumbnail_image="https://picsum.photos/300/200",  # TODO fix
                summary=body["summary"],
                body=body["body"],
                archived=body["archived"],
            )

            bp.save()

            return JsonResponse({"id": bp.id, "bp": blog_post_dict(bp)})
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
