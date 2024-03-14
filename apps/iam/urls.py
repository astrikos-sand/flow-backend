from django.urls import path, include

from apps.iam.views import router

urlpatterns = [
    path("", include(router.urls)),
]
