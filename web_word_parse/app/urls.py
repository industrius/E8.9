from django.urls import path
from .views import TaskView, ResultView, count_results, add_result

urlpatterns = [
    path("", TaskView.as_view(), name="task"),
    path("result", ResultView.as_view()),
    path("count", count_results),
    path("add_result", add_result)
]