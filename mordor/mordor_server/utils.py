import os
from django.core.exceptions import PermissionDenied
from django.http import Http404

DATA_LOCATION = r'/home/skyman/projects/mordor2/data'


def get_path(request, path):
    if not request.user.is_staff:
        tokenized = request.get_full_path().split('/')
        for p in tokenized:
            if p[0] == '.':
                raise PermissionDenied

    request_path = os.path.join(DATA_LOCATION, path)
    if not os.path.exists(request_path):
        raise Http404()

    return request_path
