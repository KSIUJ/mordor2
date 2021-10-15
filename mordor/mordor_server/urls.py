from django.urls import path
from . import views

urlpatterns = [
    path(r'list/', views.list_directory),
    path(r'list/<path:path>', views.list_directory),
    path(r'download/directory/<path:path>', views.download_directory),
    path(r'download/file/<path:path>', views.download_file),
    path(r'add/file/<path:path>', views.add_file),
    path(r'view/<path:path>', views.view_file),
]
