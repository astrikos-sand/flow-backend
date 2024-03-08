from django.urls import path, include

from apps.resource.views import router

urlpatterns = [
    path("", include(router.urls)),
]
