import os
from django.http import HttpResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from shutil import make_archive

DATA_LOCATION = r'/home/skyman/projects/mordor2/data'


# Create your views here.
def list_directory(request, path=''):
    request_path = os.path.join(DATA_LOCATION, path)
    data_in_directory = os.listdir(request_path)

    return render(request, 'mordor_server/file_list.html', {
        'files': data_in_directory
    })
    # return HttpResponse(' '.join(data_in_directory))


def download_directory(request, path):
    request_path = os.path.join(DATA_LOCATION, path)

    make_archive(r'/home/skyman/projects/mordor2/mordor2.0/mordor/mordor_server/temp/x', 'zip', request_path)
    return FileResponse(open(r'/home/skyman/projects/mordor2/mordor2.0/mordor/mordor_server/temp/x.zip', 'rb'),
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


def homepage(request):
    return render(request, 'mordor_server/home.html')