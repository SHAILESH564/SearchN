from django.shortcuts import render
from django.http import HttpResponseServerError
from .tasks import run_crawler_task_celery
from django.core.paginator import Paginator
from .models import SearchN

from django.http import JsonResponse
from django.template.loader import render_to_string   

def search(request):
    images = []
    if request.method == 'POST':
        query = request.POST.get('query', '')
        print(f"Search query: {query}")
        SearchN.objects.all().delete()  # Clear previous search results
        # run_crawler_task(query)  # Start the ?background task

        run_crawler_task_celery.delay(query)  # Start the Celery task
        # Dummy placeholders while background runs
        SearchN.objects.create(
            name="Home",
            link="images/Home.png",
            url="images/Home.png",
            is_remote=False
        )
        SearchN.objects.create(
            name="Moon",
            link="images/Moon.png",
            url="images/Moon.png",
            is_remote=False
        )
        images = SearchN.objects.order_by('-date_added')
    else:
        # Load from session if this is a GET request (for pagination)
        images = SearchN.objects.order_by('-date_added')
        # images = request.session.get('search_results', [])
    
    # Paginator is used to paginate the results
    page = Paginator(images, 9)
    page_number = request.GET.get('page')
    page_obj = page.get_page(page_number)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('image_list.html', {'page_obj': page_obj, 'images': images})
        return JsonResponse({'html': html})
    else:
        try:
            return render(request, 'searchN.html', { 'page_obj': page_obj , 'images': images})
        except Exception as e:
            return HttpResponseServerError(f"Something broke: {e}")
        
def get_count(request):
    return JsonResponse({'count': SearchN.objects.count()})