from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect

# Create your views here.
def search(request):
    context ={'job': '','place': ''}
    return render(request, "search/search_home.html",context)

def get_query(request):

    context = {'job':request.GET['job']}

    return render(request, "search/search_result.html",context)