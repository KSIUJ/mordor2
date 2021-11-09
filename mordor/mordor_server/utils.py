from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.conf import settings


def get_path(request, path):
    if not request.user.is_staff:
        tokenized = request.get_full_path().split('/')
        for p in tokenized:
            if p and p[0] == '.':
                raise PermissionDenied

    # change path from absolute to relative path
    if path and path[0] == '/':
        path = ''

    request_path = settings.MEDIA_ROOT.joinpath(path)

    if not request_path.exists():
        raise Http404()

    return request_path
