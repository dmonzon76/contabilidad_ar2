from django.shortcuts import render, redirect, get_object_or_404
from fiscal.models import AFIPActivity
from fiscal.forms import AFIPActivityForm


def afip_activity_list(request):
    activities = AFIPActivity.objects.all().order_by("code")
    return render(request, "fiscal/afip_activity_list.html", {"activities": activities})


def afip_activity_create(request):
    if request.method == "POST":
        form = AFIPActivityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("afip_activity_list")
    else:
        form = AFIPActivityForm()

    return render(request, "fiscal/afip_activity_form.html", {"form": form})


def afip_activity_edit(request, activity_id):
    activity = get_object_or_404(AFIPActivity, id=activity_id)

    if request.method == "POST":
        form = AFIPActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            return redirect("afip_activity_list")
    else:
        form = AFIPActivityForm(instance=activity)

    return render(request, "fiscal/afip_activity_form.html", {"form": form})


def afip_activity_delete(request, activity_id):
    activity = get_object_or_404(AFIPActivity, id=activity_id)
    activity.delete()
    return redirect("afip_activity_list")
