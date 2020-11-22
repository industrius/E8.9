from django.views.generic import CreateView, ListView
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import Task, Result
from .forms import TaskForm
from .tasks import parse


class TaskView(CreateView):
    """
    Отображение и обработка формы ввода новой задачи
    """
    model = Task
    form_class = TaskForm
    success_url = "/"
    template_name = "task.html"
    context_object_name = "tasks"

    def form_valid(self, form):
        task = form.save()
        parse.delay(task.pk, task.word)
        return super().form_valid(form)

class ResultView(ListView):
    """
    Эндпоинт /result для отображения списка результатов выполненых задач
    """
    template_name = "result.html"
    model = Result
    context_object_name = "results"

def count_results(request):
    """
    Эндпоинт /count для JS скрпта обработки обновления result.html странички
    по изменению количества записей в модели Result
    """
    result_count = Result.objects.all().count()
    return HttpResponse(result_count)

@csrf_exempt
def add_result(request):
    """
    Эндпоинт /add_result для consumer, обработка добавления 
    результата выполения задачи в модель Result 
    """
    if request.method == "POST":
        result = Result.objects.create(
            address=request.POST["address"],
            word=request.POST["word"],
            words_count=request.POST["words_count"],
            http_status_code=request.POST["http_status_code"]
        )
        return HttpResponse(content=result, status=201)
    else:
        return HttpResponse(status=405)