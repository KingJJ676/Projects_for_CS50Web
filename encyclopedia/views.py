from django.http import HttpResponseRedirect
import markdown
import random as rd
from django.shortcuts import render
from django.urls import reverse
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry = util.get_entry(title)
    if entry is not None:
        entry = markdown.markdown(entry)
        return render(request, 'encyclopedia/entry.html', {
            'entry': entry,
            'title': title
        })
    else:
        return render(request, 'encyclopedia/notfound.html')

def search(request):
    if request.method == 'GET':
        title = request.GET.get('q')
        entry = util.get_entry(title)
        if entry is not None:
            entry = markdown.markdown(entry)
            return render(request, 'encyclopedia/entry.html', {
                'entry': entry,
                'title': title
            })
        else:
            return render(request, 'encyclopedia/subquery.html', {
                'query': title,
                'entries': util.list_entries()
            })
    else:
        raise ValueError('Could not get website.')

def create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        titles = util.list_entries()
        if title in titles:
            return render(request, 'encyclopedia/error.html')
        content = request.POST.get('content')
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse('entry', args=[title]))
    else:
        return render(request, 'encyclopedia/create.html')
    
def edit(request, title):
    if request.method == 'GET':
        content = util.get_entry(title)
        return render(request, 'encyclopedia/edit.html', {
            'title': title,
            'content': content
        })
    else:
        newContent = request.POST.get('newContent')
        util.save_entry(title, newContent)
        return HttpResponseRedirect(reverse('entry', args=[title]))
    
def random(request):
    entries = util.list_entries()
    title = rd.choice(entries)
    return HttpResponseRedirect(reverse('entry', args=[title]))