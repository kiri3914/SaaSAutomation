from django.urls import path
from .views import FindUserView

urlpatterns = [
    path("find-user/", FindUserView.as_view(), name="find_user"),
]