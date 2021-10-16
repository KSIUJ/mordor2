import os
import markdown

from django.http import HttpResponse, FileResponse, Http404, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render
from django.template import loader

from shutil import make_archive
from shutil import rmtree

DATA_LOCATION = r'/home/bubuss/mordor2.0/data'

# Create your views here.
def list_directory(request, path=''):
    request_path = get_path(path)
    data_in_directory = os.listdir(request_path)
    
    return HttpResponse(' '.join(data_in_directory))


def download_directory(request, path):
    request_path = get_path(path)
    make_archive(r'/home/bubuss/mordor2.0/temp/x', 'zip', request_path)
    
    return FileResponse(open(r'/home/bubuss/mordor2.0/temp/x.zip', 'rb'),
                        as_attachment=True)


def download_file(request, path):
    request_path = get_path(path)
    
    return FileResponse(open(request_path, 'rb'), as_attachment=True)


@csrf_exempt
def add_file(request, path):  
    request_path = get_path(path)

    if request.method == 'POST':
        file = request.FILES['file'].open()

        f = open(request_path + file.name, 'wb')
        f.write(file.read())

        f.close()
        return HttpResponse("Done")
    else:
        return HttpResponse("Wrong request method!")


def remove_directory(request, path):
    request_path = get_path(path)
    rmtree(request_path)
    return HttpResponse("Directory removed", status=200)


def remove_file(request, path):
    request_path = get_path(path)
    os.remove(request_path)
    return HttpResponse("File removed", status=200)


def view_file(request, path):
    request_path = get_path(path)
    file_type = path[path.rindex('.')+1:]

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


def get_path(path):
    request_path = os.path.join(DATA_LOCATION, path)

    if not os.path.exists(request_path):
        raise Http404()

    return request_path
