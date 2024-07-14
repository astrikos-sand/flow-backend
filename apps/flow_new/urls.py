from django.urls import path, include

from apps.flow_new.views import SaveAPIView
from apps.flow_new.views import router

urlpatterns = [
    path("v2/", include(router.urls)),
    path("v2/save/", SaveAPIView.as_view(), name="save"),
]
