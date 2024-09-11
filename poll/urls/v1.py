from django.urls import include, path
from rest_framework.routers import DefaultRouter

from poll.views import ChoiceViewSet, PollViewSet

router = DefaultRouter()
router.register("choice", ChoiceViewSet)
router.register("poll", PollViewSet)


app_name = "poll"
urlpatterns = [
    # path("", PollsView.as_view(), name="poll-list"),
    # path("<int:pk>/", PollView.as_view(), name="poll-detail"),
    path("", include(router.urls)),
]
