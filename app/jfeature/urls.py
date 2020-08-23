from django.urls import path, include

from jfeature import views

app_name = 'feature'
urlpatterns = [
    path('create/', views.upsert, name='create')
]