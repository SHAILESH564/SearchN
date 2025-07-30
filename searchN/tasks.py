# from background_task import background
from .crawler import Crawler
from celery import shared_task


# USING background_task for running tasks in the background
# @background(schedule=1)
# def run_crawler_task(tags):    
#     try:
#         crawler = Crawler(tags)
#         smallest_tag = crawler.returnSmallestCountTag()
#         print(f"Smallest tag: {smallest_tag}")
#         crawler.search_main_tag(smallest_tag)
#     except Exception as e:
#         print(f"Error in run_crawler_task: {str(e)}")

@shared_task
def run_crawler_task_celery(tags):
    try:
        crawler = Crawler(tags)
        smallest_tag = crawler.returnSmallestCountTag()
        print(f"Smallest tag: {smallest_tag}")
        crawler.search_main_tag(smallest_tag)
    except Exception as e:
        print(f"Error in run_crawler_task_celery: {str(e)}")