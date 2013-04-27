# coding: utf-8
from __future__ import absolute_import
from django.utils.translation import ugettext as _
from django import http, template, forms
from django.shortcuts import redirect, render, render_to_response, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms.formsets import formset_factory
import uploads.models as umodels
from django.utils.timezone import now

@login_required
def list_own(request):
    areas = umodels.Area.objects.filter(owner=request.user, expiry__gte=now().date()).order_by("name")
    return render(request, "uploads/list.html", {
        "areas": areas,
    })
