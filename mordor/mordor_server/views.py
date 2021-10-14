from django.shortcuts import render
from django.http import HttpResponse, FileResponse
import os
from shutil import make_archive
import secrets
from django.core.files.temp import NamedTemporaryFile
from wsgiref.util import FileWrapper


DATA_LOCATION = r'/home/skyman/projects/mordor2/data'


# Create your views here.
def list_directory(request, path):
    request_path = DATA_LOCATION + '/' + str(path)
    data_in_directory = os.listdir(request_path)

    return HttpResponse(' '.join(data_in_directory))


def download_directory(request, path):
    request_path = DATA_LOCATION + '/' + str(path)

    make_archive(r'/home/skyman/projects/mordor2/mordor2.0/mordor/mordor_server/temp/x', 'zip', request_path)
    return FileResponse(open(r'/home/skyman/projects/mordor2/mordor2.0/mordor/mordor_server/temp/x.zip', 'rb'), as_attachment=True)


def download_file(request, path):
    request_path = DATA_LOCATION + '/' + str(path)
    print(request_path)
    return FileResponse(open(request_path, 'rb'), as_attachment=True)

