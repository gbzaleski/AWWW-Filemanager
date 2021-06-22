from django.shortcuts import render, redirect
from .models import *
from django.views.generic import ListView, CreateView
from django.forms import ModelForm
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.clickjacking import xframe_options_exempt 
from django.http import JsonResponse
from django.core.files.base import ContentFile

def home(request):
    try:
        context = {
            'files': File.objects.filter(owner = request.user),
            'directories': Directory.objects.filter(owner = request.user),
        }
    except TypeError:
        context = {}
    return render(request, 'util/base.html', context)

def add_file(request):
    return render(request, 'util/add_file.html')

def add_dir(request):
    return render(request, 'util/directory_form.html')

@xframe_options_exempt
def delete(request):
    if request.POST:
        if request.POST.get('dirs', False):
            try: 
                to_del = Directory.objects.filter(owner = request.user).get(id = request.POST['dirs'])
                to_del.deleted = True
                to_del.save()
            except ObjectDoesNotExist:
                return redirect('/delete/')
            
        if request.POST.get('files', False):
            try:
                to_del = File.objects.filter(owner = request.user).get(id = request.POST['files'])
                to_del.deleted = True
                to_del.save()
            except ObjectDoesNotExist:
                return redirect('/delete/')

        return redirect('/delete/')

    context = {
        'files': File.objects.filter(owner = request.user),
        'directories': Directory.objects.filter(owner = request.user),
    }
    return render(request, 'util/delete.html', context)

def edit_code(request):
    if request.method == 'POST' and request.is_ajax():
        try:
            to_edit = File.objects.filter(owner = request.user).get(pk = int(request.POST['fileid']))
            to_edit.content.value = request.POST['newcontent']
            to_edit.content.save(to_edit.name, ContentFile(request.POST['newcontent']))
            to_edit.save(update_fields = ['content'])
            return JsonResponse({'status':'Success', 'msg': 'File updated!'})
        except ObjectDoesNotExist:
            return JsonResponse({'status':'Fail', 'msg': 'Object does not exist'})
    else:
        return JsonResponse({'status':'Fail', 'msg':'Not a valid request'})

def open_file(request):
    return render(request, 'util/open-file.html')

def update_frama(request):
    if request.method == 'POST' and request.is_ajax():
        try:
            to_edit = File.objects.filter(owner = request.user).get(pk = int(request.POST['fileid']))
            to_edit.framapath = request.POST['framapath']
            to_edit.save(update_fields = ['framapath'])
            return JsonResponse({'status':'Success', 'msg': 'Launched frama succesfully'})
        except ObjectDoesNotExist:
            return JsonResponse({'status':'Fail', 'msg': 'Object does not exist'})
    else:
        return JsonResponse({'status':'Fail', 'msg':'Not a valid request'})