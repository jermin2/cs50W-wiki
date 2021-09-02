from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import markdown2
from . import util
from django.urls import reverse

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
    return render(request, "encyclopedia/page.html",{
        "title": title,
        "contents": markdown2.markdown(util.get_entry(title)) 
    })
    # return HttpResponse(markdown2.markdown(util.get_entry(title))  )

