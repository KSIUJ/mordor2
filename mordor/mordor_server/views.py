import os
from shutil import make_archive
from shutil import rmtree

import markdown
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, FileResponse, HttpResponseNotFound
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from .utils import get_path


# Create your views here.
def home(request, path=''):
    return render(request, "mordor_server/home.html")


def list_directory(request, path=''):
    if not request.user.is_authenticated:
        raise PermissionDenied

    request_path = get_path(request, path)
    data_in_directory = os.listdir(request_path)

    hidden_files = [x for x in data_in_directory if os.path.isfile(os.path.join(request_path, x)) and x[0] == '.']
    hidden_directories = [x for x in data_in_directory if os.path.isdir(os.path.join(request_path, x)) and x[0] == '.']
    files = [x for x in data_in_directory if os.path.isfile(os.path.join(request_path, x)) and x not in hidden_files]
    directories = [x for x in data_in_directory if os.path.isdir(os.path.join(request_path, x)) and x not in hidden_directories]

    return render(request, 'mordor_server/file_list.html', {
        'hidden_files': hidden_files,
        'hidden_directories': hidden_directories,
        'files': files,
        'directories': directories,
        'path': path
    })


def download_directory(request, path):
    if not request.user.is_authenticated:
        raise PermissionDenied

    request_path = get_path(request, path)
    make_archive(r'/home/skyman/projects/mordor2/data/temp/x', 'zip', request_path)

    return FileResponse(open(r'/home/skyman/projects/mordor2/data/temp/x.zip', 'rb'),
                        as_attachment=True)


def download_file(request, path):
    if not request.user.is_authenticated:
        raise PermissionDenied

    request_path = get_path(request, path)

    return FileResponse(open(request_path, 'rb'), as_attachment=True)


@csrf_exempt
def add_file(request, path):
    if not request.user.is_staff:
        raise PermissionDenied

    request_path = get_path(request, path)

    if request.method == 'POST':
        file = request.FILES['file'].open()

        f = open(request_path + file.name, 'wb')
        f.write(file.read())

        f.close()
        return HttpResponse("Done")
    else:
        return HttpResponse("Wrong request method!")


def remove_directory(request, path):
    if not request.user.is_staff:
        raise PermissionDenied

    request_path = get_path(request, path)
    rmtree(request_path)
    return HttpResponse("Directory removed", status=200)


def remove_file(request, path):
    if not request.user.is_staff:
        raise PermissionDenied

    request_path = get_path(request, path)
    os.remove(request_path)
    return HttpResponse("File removed", status=200)


def view_file(request, path):
    if not request.user.is_authenticated:
        raise PermissionDenied

    request_path = get_path(request, path)
    file_type = path[path.rindex('.') + 1:]

    if file_type.lower() == "md":
        file = open(request_path, 'r')
        html = markdown.markdown(file.read(), extensions=['extra'])
        return render(request, 'mordor_server/index.html', {'markdown': html})
    else:
        return FileResponse(open(request_path, 'rb'))


def handler403(request, exception):
    content = loader.render_to_string('mordor_server/home.html', {}, request)
    return HttpResponseNotFound(content)


def handler404(request, exception):
    content = loader.render_to_string('mordor_server/home.html', {}, request)
    return HttpResponseNotFound(content)


def handler500(request):
    content = loader.render_to_string('mordor_server/home.html', {}, request)
    return HttpResponseNotFound(content)
