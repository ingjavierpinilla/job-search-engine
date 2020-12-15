from django.shortcuts import render
from django.http import HttpResponseRedirect

# Create your views here.
def home(request):
    context={'asd':12}
    return render(request, "search/index.html", context)

def search_bar(request):
    print(request)
    if request.method == "POST":
        current_date = timezone.now()
        content = request.POST["content"]
        
    return HttpResponseRedirect("/")