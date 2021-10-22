import markdown

from pathlib import Path
from shutil import make_archive
from shutil import rmtree

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, FileResponse, HttpResponseNotFound
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from .utils import get_path


# Create your views here.
def home(request, path=''):
    return render(request, "mordor_server/home.html")

@csrf_exempt
def list_directory(request, path=''):
    if not request.user.is_authenticated and not settings.DEBUG:
        raise PermissionDenied

    request_path = get_path(request, path)
    directory = [f for f in request_path.iterdir()]

    hidden_files = [f.name for f in directory if f.is_file() and f.name[0] == '.']
    hidden_directories = [f.name for f in directory if f.is_dir() and f.name[0] == '.']
    files = [f.name for f in directory if f.is_file() and f.name not in hidden_files]
    directories = [f.name for f in directory if f.is_dir() and f.name not in hidden_directories]    

    return render(request, 'mordor_server/file_list.html', {
        'hidden_files': hidden_files,
        'hidden_directories': hidden_directories,
        'files': files,
        'directories': directories,
        'path': path
    })


def download_directory(request, path):
    if not request.user.is_authenticated and not settings.DEBUG:
        raise PermissionDenied

    request_path = get_path(request, path)
    print(request_path)
    make_archive(settings.MEDIA_ROOT.joinpath(request_path.name), 'zip', request_path)

    return FileResponse(open(settings.MEDIA_ROOT.joinpath(request_path.name+".zip"), 'rb'),
                        as_attachment=True)


def download_file(request, path):
    if not request.user.is_authenticated and not settings.DEBUG:
        raise PermissionDenied

    request_path = get_path(request, path)

    return FileResponse(open(request_path, 'rb'), as_attachment=True)


@csrf_exempt
def add_file(request, path):
    if not request.user.is_staff and not settings.DEBUG:
        raise PermissionDenied

    request_path = get_path(request, path)

    if request.method == 'POST':
        file = request.FILES['file'].open()

        request_path = request_path.joinpath(file.name)
        with request_path.open(mode='wb') as f:
            f.write(file.read())

        return HttpResponse("Done")
    else:
        return HttpResponse("Wrong request method!")


def remove_directory(request, path):
    if not request.user.is_staff and not settings.DEBUG:
        raise PermissionDenied

    request_path = get_path(request, path)
    rmtree(request_path)
    return HttpResponse("Directory removed", status=200)


def remove_file(request, path):
    if not request.user.is_staff and not settings.DEBUG:
        raise PermissionDenied

    request_path = get_path(request, path)
    request_path.unlink(missing_ok=True)

    return HttpResponse("File removed", status=200)


def view_file(request, path):
    if not request.user.is_authenticated and not settings.DEBUG:
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
