from django.urls import path, include

from apps.resource.views import router
from apps.resource.views import FileUploadView, DataStoreAPIView

urlpatterns = [
    path("", include(router.urls)),
    path("upload/csv/", FileUploadView.as_view(), name="file-upload"),
    path("datastore/", DataStoreAPIView.as_view(), name="datastore"),
]
