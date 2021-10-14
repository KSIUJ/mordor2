from django.urls import path
from .views import *

urlpatterns = [
    path(r'list/<path:path>', list_directory),
    path(r'download/directory/<path:path>', download_directory),
    path(r'download/file/<path:path>', download_file),
]
