from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
generic.edit.FormMixin
from pricedb.models import PriceDb, SalesPrice


class IndexView(generic.ListView):
    template_name = 'pricedb/index.html'
    context_object_name = 'price_set'
    model = PriceDb

    # def get_queryset(self):
    #     """Return the last five published questions."""
    #     return PriceDb.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = PriceDb
    template_name = 'pricedb/details.html'
    context_object_name = 'price_list'

    def get_context_data(self, **kwargs):
        pass
# class ResultsView(generic.DetailView):
#     model = PriceDb
#     template_name = 'pricedb/index.html'
#     context_object_name = 'price_set'


# def vote(request, question_id):
#     # same as above, no changes needed.
#     pass
