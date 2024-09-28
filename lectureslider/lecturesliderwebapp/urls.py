from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("convert/<int:vid_id>/", views.convert, name="convert"),
    path("download/<path:file_path>/", views.download, name="download"),
]

