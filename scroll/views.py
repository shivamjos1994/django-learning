from django.shortcuts import render
from django.http import JsonResponse
import time

# Create your views here.
def index(request):
    return render(request, "posts/index.html")


def posts(request):
    # get start and end points
    start = int(request.GET.get("start") or 0)
    end = int(request.GET.get("end") or (start + 9))

    # generate list of posts
    data = []
    for i in range(start, end + 1):
        data.append(f"Post #{i}")

    # artificially delay speed of response
    time.sleep(1)
    
    #return list of posts
    return JsonResponse({"posts": data})