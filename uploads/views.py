# coding: utf-8
from __future__ import absolute_import
from django.utils.translation import ugettext as _
from django import http, template, forms
from django.shortcuts import redirect, render, render_to_response, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms.formsets import formset_factory
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
import uploads.models as umodels
from django.utils.timezone import now
import datetime

@login_required
def list_own(request):
    areas = umodels.Area.objects.filter(owner=request.user, expiry__gte=now().date()).order_by("name")
    return render(request, "uploads/list.html", {
        "areas": areas,
    })

class AreaForm(forms.ModelForm):
    expiry = forms.DateField(required=True,
                             initial=now,
                             input_formats=("%Y-%m-%d",),
                             widget=forms.DateInput(format="%Y-%m-%d"))

class AreaCreateForm(AreaForm):
    class Meta:
        model = umodels.Area
        exclude = ('owner', 'uuid')

    def validate_unique(self):
        exclude = self._get_validation_exclusions()
        exclude.remove("owner")
        try:
            self.instance.validate_unique(exclude=exclude)
        except forms.ValidationError, e:
            self._update_errors(e.message_dict)

class AreaEditForm(AreaForm):
    class Meta:
        model = umodels.Area
        exclude = ('owner', 'name', 'uuid')

    def validate_unique(self):
        exclude = self._get_validation_exclusions()
        exclude.remove("owner")
        try:
            self.instance.validate_unique(exclude=exclude)
        except forms.ValidationError, e:
            self._update_errors(e.message_dict)

class AreaCreate(CreateView):
    model = umodels.Area
    form_class = AreaCreateForm
    success_url = reverse_lazy("uploads_list")

    def get_initial(self):
        initial = super(AreaCreate, self).get_initial().copy()
        initial["expiry"] = now().date() + datetime.timedelta(days=30)
        return initial

    def get_form(self, form_class):
        form = super(AreaCreate, self).get_form(form_class)
        form.instance.owner = self.request.user
        return form

    def form_valid(self, form):
        import uuid
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.uuid = str(uuid.uuid4())
        self.object.save()
        return redirect(self.get_success_url())

class AreaUpdate(UpdateView):
    model = umodels.Area
    form_class = AreaEditForm
    success_url = reverse_lazy("uploads_list")

class AreaDelete(DeleteView):
    model = umodels.Area
    success_url = reverse_lazy("uploads_list")

