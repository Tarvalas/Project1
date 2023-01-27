from django.http import HttpResponse
from django.shortcuts import render, redirect
from markdown2 import Markdown
from django.urls import reverse
import random
import os

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    raw_entry = util.get_entry(title)
    if raw_entry:
        html_entry = Markdown().convert(raw_entry)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": html_entry,
            })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": "404 - Not Found",
            "entry": "404 - Page not found. Check URL and retry.",
        })

def search(request):
    query = request.POST['q']
    raw_entry = util.get_entry(query)

    if raw_entry:
        return redirect('entry', title=query)
    else:
        search_results = util.get_similar(query)
        return render(request, 'encyclopedia/search.html', {
            "search_results": search_results,
        })

def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        raw_entry = request.POST["entry"]

        util.save_entry(title, raw_entry)
        return redirect('entry', title=title)
    else:
        return render(request, "encyclopedia/create.html")

def random_page(request):
    page = random.choice(util.list_entries())
    return redirect('entry', title=page)

def edit(request, title, flag=False):
    if request.method == "POST":
        new_title = request.POST["title"]
        if new_title:
            raw_entry = request.POST["entry"]
            util.save_entry(new_title, raw_entry, title)
            return redirect('entry', title=new_title)
        else:
            entry = util.get_entry(title)
            return render(request, "encyclopedia/edit.html", {
                "title": title,
                "entry": entry,
                "flag": True,
            })
    else:
        entry = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "entry": entry,
        })