from django.urls import path, include

from apps.flow.views import (
    router,
    SaveAPIView,
    SaveCodeFileAPIView
)

urlpatterns = [
    path("", include(router.urls)),
    path("save/", SaveAPIView.as_view(), name="save"),
    path("file-upload/", SaveCodeFileAPIView.as_view(), name="new-node"),
]
