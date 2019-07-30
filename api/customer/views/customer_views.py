import json

from django.http import JsonResponse
from django.urls import reverse
from customer.models import Customer


def customer_index(request):
    data = json.loads(request.body.decode('utf-8'))
    custoemr_name = data['name']
    # customers = Customer.objects.filter(name__contains=custoemr_name)
    customers = Customer.objects.order_by('name')

    context = {
        'customers': [
            {'id': customer.pk, 'name': customer.name} for customer in customers
        ]
    }
    return JsonResponse(context, safe=False)

