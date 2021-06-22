from django.shortcuts import render, redirect
from .models import *
from django.views.generic import ListView, CreateView
from django.forms import ModelForm
from django.core.exceptions import ObjectDoesNotExist

class DirectoryCreateView(CreateView):
    model = Directory
    fields = ['name', 'description']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class FileForm(ModelForm):
    class Meta:
        model = File
        fields = ['name', 'owner', 'directory', 'content', 'description']

    def __init__(self, *args, **kwargs):
        owner = kwargs.pop('owner')
        super(FileForm, self).__init__(*args, **kwargs)
        self.fields['directory'].queryset = Directory.objects.filter(owner = owner).filter(deleted = False)
        self.fields['owner'].queryset = User.objects.filter(id = owner.id)

class FileCreateView(CreateView):
    form_class = FileForm
    template_name = 'util/file_form.html'

    def get_form_kwargs(self):
        kwargs = super(FileCreateView, self).get_form_kwargs()
        kwargs['owner'] = self.request.user
        return kwargs