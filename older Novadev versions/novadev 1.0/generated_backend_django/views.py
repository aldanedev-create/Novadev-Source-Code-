"""Generated NovaDev 0.5 Django view starter."""

from django.http import JsonResponse

RESOURCES = {'posts': 'Post'}


def health(request):
    return JsonResponse({"ok": True, "backend": "Django"})
