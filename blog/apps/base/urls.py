from django.urls import path
from . import views

app_name = 'base'

urlpatterns = [
    path('', views.index, name='index'),
    path('get-user-data', views.get_user_data, name='get-user-data'),
    path('get-entries-list', views.get_entries_list, name='get-entries-list'),
]
