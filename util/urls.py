from django.urls import path
from . import views
from .views import *
from .forms import *

urlpatterns = [
    path('', views.home, name='util-home'),
    path('add-file/', FileCreateView.as_view(), name='util-add-file'),
    path('add-dir/', DirectoryCreateView.as_view(), name='util-add-directory'),
    path('delete/', views.delete, name='util-delete'),
    path('open-file/', views.open_file, name='util-open-file'),
    path('update-frama/', views.update_frama, name='util-update'),
    path('edit-code/', views.edit_code, name='util-edit-code'),
]
