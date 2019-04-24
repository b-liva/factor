from random import randint
from django.test import TestCase
from django.urls import reverse

from customer.models import Customer, Type
from request.models import Requests, Xpref, ReqSpec, PrefSpec
from django.utils import timezone
from django_jalali import models as jmodels
from accounts.models import User


class RequestListVeiwTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # create 10 users
        number_of_user = 10
        for user_id in range(number_of_user):
            User.objects.create(
                username=f"username{user_id}",
                first_name=f"firstname{user_id}",
                last_name=f"lastname{user_id}",
                email=f"email{user_id}@gmail.com"
            )
            print('user was created.')
            rnd = randint(1, User.objects.all().count())
            print(rnd)
            # print(User.objects.get(pk=5))
        # create customer types
        # customer_types = ['مستقل', 'آبفا', 'فولاد', 'نفت و گاز', 'پتروشیمی','سیمان']
        customer_types = ['type01', 'type01', 'type01', 'type01', 'type01', 'type01']
        for customer_type in customer_types:
            Type.objects.create(
                name=customer_type
            )
        # print(User.objects.get(pk=5))
        # create 10 customers
        number_of_customers = 5
        for customer_id in range(number_of_customers):
            Customer.objects.create(
                owner=User.objects.get(id=randint(1, User.objects.all().count())),
                user=User.objects.get(id=randint(1, User.objects.all().count())),
                name=f"name{customer_id}",
                code=f"{customer_id}",
                pub_date=timezone.now(),
                type=Type.objects.get(id=randint(1, Type.objects.all().count()))
            )
        # create 100 requests for paginaton tests
        number_of_requests = 100
        for req_id in range(number_of_requests):
            Requests.objects.create(
                owner=User.objects.get(id=randint(1, User.objects.all().count())),
                customer=Customer.objects.get(id=randint(1, Customer.objects.all().count())),
                number=req_id,
                pub_date=timezone.now(),
                date_fa=timezone.now(),
            )

    def test_create_request(self):
        reqs = Requests.objects.all()
        self.assertEqual(reqs.count(), 100)
