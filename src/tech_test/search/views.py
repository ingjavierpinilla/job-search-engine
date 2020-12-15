from django.shortcuts import render
from django.http import HttpResponseRedirect

# Create your views here.
def home(request):

    return render(request, "search/index.html")

def search_bar(request):
    print(request)
    if request.method == "POST":
        current_date = timezone.now()
        content = request.POST["content"]

    return HttpResponseRedirect("/")