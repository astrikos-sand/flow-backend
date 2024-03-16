from django.urls import path, include

from apps.flow.views import router

urlpatterns = [
    path("", include(router.urls)),
]
