import os
import markdown

from django.http import HttpResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from shutil import make_archive
from django.shortcuts import render

DATA_LOCATION = r'/home/bubuss/mordor2.0/data'


# Create your views here.
def list_directory(request, path=''):
    request_path = os.path.join(DATA_LOCATION, path)
    data_in_directory = os.listdir(request_path)

    return HttpResponse(' '.join(data_in_directory))


def download_directory(request, path):
    request_path = os.path.join(DATA_LOCATION, path)

    make_archive(r'/home/bubuss/mordor2.0/temp/x', 'zip', request_path)
    return FileResponse(open(r'/home/bubuss/mordor2.0/temp/x.zip', 'rb'),
                        as_attachment=True)


def download_file(request, path):
    request_path = os.path.join(DATA_LOCATION, path)

    return FileResponse(open(request_path, 'rb'), as_attachment=True)

@csrf_exempt
def add_file(request, path):
    request_path = os.path.join(DATA_LOCATION, path)

    if request.method == 'POST':
        file = request.FILES['file'].open()

        f = open(request_path + file.name, 'wb')
        f.write(file.read())

        f.close()
        return HttpResponse("Done")
    else:
        return HttpResponse("Wrong request method!")


def view_file(request, path):
    request_path = DATA_LOCATION + '/' + str(path)
    file_type = path[path.rindex('.')+1:]

    if file_type.lower() == "md":
        file = open(request_path, 'r')
        html = markdown.markdown(file.read(), extensions=['fenced_code'])
        return render(request, 'mordor_server/index.html', {'markdown': html})
    else:
        return FileResponse(open(request_path, 'rb'))