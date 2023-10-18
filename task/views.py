from django.shortcuts import render, redirect
from django import forms



class NewTaskForm(forms.Form):
     task = forms.CharField(label="New Task")



# Create your views here.
def index(request):
    if "tasks" not in request.session:
        request.session["tasks"] = []
    context = {'tasks': request.session["tasks"]}
    return render(request, "index.html", context)


def add_task(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data["task"]
            request.session["tasks"] += [task]
            return redirect("/index")
        else:
            return render(request, "add_tasks.html", {'form': form})

    context = {"form": NewTaskForm()}
    return render(request, "add_tasks.html", context)
