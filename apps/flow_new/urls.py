from django.urls import path, include

from apps.flow_new.views import router

urlpatterns = [
    path("", include(router.urls)),
]
