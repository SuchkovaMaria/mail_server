from django.urls import path

from service.apps import ServiceConfig
from service.views import StartView

app_name = ServiceConfig.name

urlpatterns = [
    path("", StartView.as_view(), name="home"),
]