from pathlib import Path
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError
from django.views import View
from .forms import ReservationForm, SearchForm
from .crawler import Crawler
from django.core.paginator import Paginator
from .models import SearchN

import requests
import os

def hello_w(request):
    return HttpResponse("Hello World")

class India(View):
    def get(self, request):
        return HttpResponse("Hello India")

def Home(request):
    form = ReservationForm()

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Form submitted successfully")
    return render(request, 'index.html', {'form': form})

# def search(request):
#     # form = SearchForm()
#     if request.method == 'POST':
#         form = SearchForm(request.POST)
#         if form.is_valid():
#             query = form.cleaned_data['query']
#             # Process the search data
#             form.save()
#             return HttpResponse(f"Search submitted successfully {query}")
#     return render(request, 'seachN.html', {'form': form})
#     # return HttpResponse("Search N")

def search(request):
    images = []
    if request.method == 'POST':
        query = request.POST.get('query', '')
        print(f"Search query: {query}")
        # return HttpResponse(f"Search submitted successfully {query}")
        SearchN.objects.all().delete()  # Clear previous search results
        crawler = Crawler(query)
        smallest_tag = crawler.returnSmallestCountTag()
        print(f"Smallest tag: {smallest_tag}")
        crawler.search_main_tag(smallest_tag)
        # for name, link, src in result.values():
        #     images.append({"url": src, 
        #                    "name": name,
        #                    "link": link,
        #                    'is_remote': src.startswith('http')})
            
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
    page_number = request.GET.get('page')
    page = Paginator(images, 10)
    page_obj = page.get_page(page_number)
        # print(f"Result: {result}")
    print(f"{page_obj} images found")
    try:
        return render(request, 'searchN.html', { 'page_obj': page_obj , 'images': images})
    except Exception as e:
        return HttpResponseServerError(f"Something broke: {e}")
    # return HttpResponse("Search N")
