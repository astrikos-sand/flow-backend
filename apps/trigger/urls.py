from django.urls import path, include

from apps.trigger.views import router

urlpatterns = [
    path("triggers/", include(router.urls)),
]
