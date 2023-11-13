from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import SiteForm


@login_required
def create_site(request):
    if request.method == "POST":
        form = SiteForm(request.POST)
        if form.is_valid():
            site = form.save(commit=False)
            site.user = request.user
            site.save()
            return redirect("home")
        else:
            print(f"Form is invalid {form.errors = }")
    else:
        form = SiteForm()
    return render(request, "sites/create_site.html", {"form": form})
