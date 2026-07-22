from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from fiscal.models.AFIPactivities import AFIPActivity
from fiscal.forms.afip_activity import AFIPActivityForm


@login_required
def afip_activity_list(request):
    activities = AFIPActivity.objects.all().order_by("code")
    return render(
        request,
        "fiscal/afip_activity_list.html",
        {
            "activities": activities,
        },
    )


@login_required
def afip_activity_create(request):
    if request.method == "POST":
        form = AFIPActivityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("fiscal:afip_activity_list")
    else:
        form = AFIPActivityForm()

    return render(
        request,
        "fiscal/afip_activity_form.html",
        {
            "form": form,
            "mode": "create",
        },
    )


@login_required
def afip_activity_edit(request, pk):
    activity = get_object_or_404(AFIPActivity, pk=pk)

    if request.method == "POST":
        form = AFIPActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            return redirect("fiscal:afip_activity_list")
    else:
        form = AFIPActivityForm(instance=activity)

    return render(
        request,
        "fiscal/afip_activity_form.html",
        {
            "form": form,
            "mode": "edit",
            "activity": activity,
        },
    )
