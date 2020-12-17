from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Job
from .API import search_job, get_aggregators
from .utils import get_query_request_handle, parse_jobs

# Create your views here.
def search(request):

    context ={'job_search': '','place_search': '', 'remote_search': ''}
    return render(request, "search/search_home.html", context)

def get_query(request):
    try:
        Job.objects.all().delete()
    except:
        pass
    context, skills_selected, types_selected = get_query_request_handle(request, get_aggregators())
    remote = False
    if context.get('remote_search') == 'checked':
        remote = True
    jobs = search_job(size = 15, remote = remote, skills = skills_selected, type = types_selected)
    
    if len(jobs) != 0:
        parse_jobs(jobs)     
        context['job_items'] = Job.objects.all()

    return render(request, "search/search_result.html",context)

