from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from .API import search_job

# Create your views here.
def search(request):
    context ={'job_search': '','place_search': '', 'remote_search': ''}
    return render(request, "search/search_home.html", context)

def get_query(request):

    job_search = request.GET.get('job_search',"")
    place_search = request.GET.get('place_search',"")
    if request.GET.get('remote_search',"") == 'on':
        remote_search = 'checked'
    else:
        remote_search = ''
    jobs = search_job(size = 6, remote = False, skills = ['Marketing', 'Communication'])
    context = {'job_search': job_search, 'place_search': place_search, 'remote_search': remote_search, 'jobs': jobs}

    return render(request, "search/search_result.html",context)