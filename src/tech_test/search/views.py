from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Job
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
    jobs = search_job(size = 9, remote = True, skills = ['Software Development'])

    context = {'job_search': job_search, 'place_search': place_search, 'remote_search': remote_search, 'jobs': jobs}

    return render(request, "search/search_result.html",context)

def parse_jobs(jobs):
    for job in jobs:
        id = job['id']
        objective = job['objective']
        type = job['type']
        organization_name = job['organizations'][0]['name']
        organization_picture = job['organizations'][0]['picture']
        locations = job['locations']
        remote = job['remote']
        if remote:
            locations.append("Remote")
        if len(locations) != 0:
            locations = ', '.join(locations)
        skills =[]
        for skill in job['skills']:
            skills.append(skill['name'])
        skills = ', '.join(skills)
        min = str(job['compensation']['data']["minAmount"])
        max = str(job['compensation']['data']["maxAmount"])
        curr = str(job['compensation']['data']["currency"])
        per = str(job['compensation']['data']["periodicity"])
        compensation = f'{min} - {max} {curr}/{per}'

        obj = Todo.objects.create(_id = id, objective = objective, type = type, organization_name = organization_name,
        organization_picture = organization_picture, locations = locations, remote = remote, skills = skills,
        compensation = compensation)