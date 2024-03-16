from django.urls import path, include

from apps.webhook.views import router

urlpatterns = [
    path("", include(router.urls)),
]
