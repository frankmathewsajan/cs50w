import random
from django import forms
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from markdown import markdown

from . import util


class SearchForm(forms.Form):
    q = forms.CharField(
        label="",
        widget=forms.TextInput(
            {"class": "search", "placeholder": "Search Encyclopedia"}
        ),
    )

class NewEntryForm(forms.Form):
    title = forms.CharField(
        label="Entry Title",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    content = forms.CharField(
        label="Content", 
        widget=forms.Textarea(attrs={"class": "form-control"})
    )


def index(request):
    return render(
        request,
        "encyclopedia/index.html",
        {"entries": util.list_entries(), "form": SearchForm(), "head": f"All Pages"},
    )

def lucky(request):
    entries = util.list_entries()
    title = random.choice(entries)
    return HttpResponseRedirect(reverse('display', args=(title,)))

def new(request):
    if request.method == 'POST':
        form = NewEntryForm(request.POST)
        entries = util.list_entries()
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            if title not in entries:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse('display', args=(title,)))
            else:
                return render(request, "encyclopedia/new.html", {
                    "new_form": form,
                    "error_message": "An entry with that title already exists.",
                    "head": 'New Entry',
                    "action":'new',
                    'title':title
                })
    return render(
        request,
        "encyclopedia/new.html",
        {"entries": util.list_entries(), "form": SearchForm(), "new_form": NewEntryForm(), "head": f"New Entry"},
    )


def edit(request, title):
    
    if request.method == 'POST':
        form = NewEntryForm(request.POST)
        entries = util.list_entries()
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            if title in entries:
                util.save_entry(title, content)
                print(title)
                return HttpResponseRedirect(reverse('display', args=(title,))) 
            else:
                return render(request, "encyclopedia/new.html", {
                    "new_form": form,
                    "error_message": "Entry with that title doesn't exist. Click Save again to create it.",
                    "head": 'Edit Entry',
                    "action":'edit',
                    "title":title
                })
            
    content = util.get_entry(title)
    return render(
        request,
        "encyclopedia/new.html",
        {
            "entries": util.list_entries(), 
            "form": SearchForm(), 
            "new_form": NewEntryForm({
                'content': content,
                'title':title
                }), 
            "head": f"Edit Entry",
            "action":'edit',
            "title":title
            },
            
    )


def search(request):
    q = request.GET.get("q", "")
    entries = util.list_entries()
    perfect_match = [i for i in entries if i.lower() == q.lower()]
    return (
        display(request, perfect_match[0])
        if perfect_match
        else render(
            request,
            "encyclopedia/index.html",
            {
                "entries": [i for i in entries if q.lower() in i.lower()],
                "form": SearchForm(),
                "head": f"Search Results for <i><a href='search?q={q}'>{q}</a></i>",
            },
        )
    )


def display(request, title):
    content = util.get_entry(title)

    if content:
        return render(
            request,
            "encyclopedia/display.html",
            {"content": markdown(content), "form": SearchForm(), "title": title},
        )
    raise Http404("Page not found")
