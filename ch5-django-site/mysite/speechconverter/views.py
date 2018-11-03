from django.shortcuts import render
from .forms import CommentForm
from django.http import HttpResponseRedirect
from django.templatetags.static import static
import os

def index(request):
    return render(request, 'speechconverter/home.html')

def analyze(request):
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, 'textfiles/file.txt')
    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            text = form.cleaned_data['comment']
        else:
            text = "broken comment"

        f = open(file_path, 'w+')
        f.write(str(text))
        f.close()

        return HttpResponseRedirect('/analyze_text')

    elif request.method == "GET":
        f = open(file_path, 'r')
        lines = f.readlines()
        f.close()
        return render(request, 'speechconverter/text_analysis.html', {'content':lines})




# Create your views here.
