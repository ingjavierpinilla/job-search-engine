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
    Job.objects.all().delete()
    parse_jobs(jobs)
    job_items = Job.objects.all()
    context = {'job_search': job_search, 'place_search': place_search, 'remote_search': remote_search, 'job_items': job_items}

    return render(request, "search/search_result.html",context)

def parse_jobs(jobs):
    for job in jobs:
        id = job.get('id')
        objective = job.get('objective')
        type = job.get('type')
        organization_name = job.get('organizations')[0].get('name')
        organization_picture = job.get('organizations')[0].get('picture')
        locations = job.get('locations')
        remote = job.get('remote')
        if remote:
            locations.append("Remote")
        if len(locations) != 0:
            locations = ', '.join(locations)
        skills =[]
        for skill in job.get('skills'):
            skills.append(skill.get('name'))
        skills = ', '.join(skills)
        if job.get('compensation').get('visible'):
            min = str(job.get('compensation').get('data').get('minAmount'))
            max = str(job.get('compensation').get('data').get('maxAmount'))
            curr = str(job.get('compensation').get('data').get('currency'))
            per = str(job.get('compensation').get('data').get('periodicity'))
            if min == 'None':
                max = max.split('.', 1)[0]
                compensation = f'{max} {curr}/{per}'
            elif max == 'None':
                min = min.split('.', 1)[0]
                compensation = f'{min} {curr}/{per}'
            else:
                min = min.split('.', 1)[0]
                max = max.split('.', 1)[0]
                compensation = f'{min} - {max} {curr}/{per}'
        else:
            compensation = ''
        obj = Job.objects.create(_id = id, objective = objective, type = type, organization_name = organization_name,
        organization_picture = organization_picture, locations = locations, remote = remote, skills = skills,
        compensation = compensation)