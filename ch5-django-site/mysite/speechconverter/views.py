from django.shortcuts import render
from .forms import CommentForm
from django.http import HttpResponseRedirect
from django.templatetags.static import static
import os
from . import language

module_dir = os.path.dirname(__file__)
def index(request):
    file_path = os.path.join(module_dir, 'textfiles/file_in.txt')
    f = open(file_path, 'r')
    lines = f.readlines()
    full_text = "".join(lines)
    f.close()
    return render(request, 'speechconverter/home.html', {'default':full_text})

def analyze(request):

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
        full_text = "".join(lines)
        f.close()


        analyzed_lines = language.return_sentiment(full_text)
        return render(request, 'speechconverter/text_analysis.html', {'original_text':full_text, 'content':analyzed_lines})




# Create your views here.
