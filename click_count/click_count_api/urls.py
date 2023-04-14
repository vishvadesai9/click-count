from os import name
from django.urls import path
from rest_framework.routers import DefaultRouter
from click_count_api.views import ClickModelView


router = DefaultRouter()


urlpatterns = [
    path("click-count/", ClickModelView.as_view(), name="click")
    ]
