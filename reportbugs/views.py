from django.shortcuts import render
from reportbugs.models import Bugs
from django.views.generic import ListView, DetailView, CreateView, UpdateView
# Create your views here.


class BugsListView(ListView):
    template_name = 'reportbugs/index.html'
    model = Bugs
