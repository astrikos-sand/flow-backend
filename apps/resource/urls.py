from django.urls import path, include

from apps.resource.views import router
from apps.resource.views import FileUploadView

urlpatterns = [
    path("", include(router.urls)),
    path("upload/csv/", FileUploadView.as_view(), name="file-upload"),
]
