from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import markdown2
from . import util
from django.urls import reverse

from django import forms

import random

# import regular expressions for query
# import re


def index(request):
    # Handle POST requests
    if request.method == "POST":
        # Check if the query exists
        query = request.POST.get("q")
        if util.get_entry(query):
            # Redirect to the correct page
            return HttpResponseRedirect( reverse("page", args=[query]))
        else:
            # Filter entries by query
            entries = util.list_entries()

            filteredEntries = filter(lambda val: query in val, entries)

            return render(request, "encyclopedia/index.html", {
                "title" : "Search Results",
                "entries" : filteredEntries,
            })
            return HttpResponse("Could not find result")
    else:
        return render(request, "encyclopedia/index.html", {
            "title": "All Pages",
            "entries": util.list_entries()
        })

def page(request, title):
    # Check if title exists
    if util.get_entry(title):
        return render(request, "encyclopedia/page.html",{
            "title": title,
            "contents": markdown2.markdown(util.get_entry(title)) 
        })
    
    # Return 404 Error
    return render(request, "encyclopedia/error.html", {
        "error_num": 404,
        "message": "Page Not Found"
    })



def add(request):
    # Handle POST requests
    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        form = NewEntryForm(request.POST)

        # Check if the form data is valid (server-side)
        if form.is_valid():

            # Isolate the data from the 'cleaned' version
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            # Check if title exists
            if util.get_entry(title):
                return render(request, "encyclopedia/error.html", {
                    "error_num": 409,
                    "message": "Entry already exists!"
                })

            # Save the new entry
            util.save_entry(title, content)

            # Redirect to the new page
            return HttpResponseRedirect( reverse("page", args=[title]))

        else:

            # If the form is invalid, re-render the page with existing information
            return render(request, "encyclopedia/add.html", {
                "form":form
            })

    else:

        return render(request, "encyclopedia/add.html", {
            "form": NewEntryForm()
        })

def edit(request, title):

    try:
        # Grab the existing data
        content = util.get_entry(title)

        form = NewEntryForm({
            "title": title,
            "content": content
        })

        return render(request, "encyclopedia/add.html", {
            "form":form
        })

    except:
        
        # Return an error if we cannot get to the edit page
        return render(request, "encyclopedia/error.html", {
            "error_num": 410,
            "message": "Entry doesn't exist"
        })

def randompage(request):
    entry = random.choice(util.list_entries())
    return HttpResponseRedirect( reverse("page", args=[entry]))

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea)
