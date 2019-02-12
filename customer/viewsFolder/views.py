import nested_dict as nd
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView
)


from customer.models import Customer
from customer.views import customers_payment
from request.views2 import total_kw
from customer.mixins import OwnRequestMixin
from request.models import (
    Requests,
    Xpref,
    Prefactor,
)
from request.forms.forms import SpecForm
from customer.forms import (
    CustomerRequestCreateForm,
    CustomerRequestFileCreateForm,
)


class CustomerRequestsListView(ListView):
    template_name = 'customer_account/details.html'
    model = Requests

    def get_queryset(self):
        customer = Customer.objects.get(user=self.request.user)
        customer_reqs = super(CustomerRequestsListView, self).get_queryset().filter(customer__user=self.request.user)\
            .order_by('date_fa').reverse()
        kwList = []
        pList = []
        totalRes = {}
        tempDict = {}
        proformaDict = {}
        for customer_req in customer_reqs:
            tempDict = {}
            tempDict['kw'] = total_kw(customer_req.pk)
            kwList.append(tempDict['kw'])
            req_profs = customer_req.xpref_set.all()
            paymentList = []
            for p in req_profs:
                proformaDict = {}
                pList.append(p)
                payments = p.payment_set.all()
                print(f'payments is: {payments}')
                for pmnt in payments:
                    paymentList.append(pmnt)
                proformaDict['payments'] = paymentList

            print(f'***payment list is: {paymentList}')

            proformaDict['proformas'] = req_profs
            reqspec = customer_req.reqspec_set.all()
            tempDict['profs'] = req_profs
            tempDict['profs2'] = proformaDict
            tempDict['specs'] = reqspec
            tempDict['req'] = customer_req
            totalRes[customer_req.pk] = tempDict

        totalpaymenst = customer.payment_set.all()
        print(f'total result: {totalRes}')
        payList = []
        for pay in totalpaymenst:
            payList.append(pay.amount)

        paySum = sum(payList)
        payment_list, payment_sum = customers_payment(customer.pk)
        request_count = customer.requests_set.count()
        response = {
            'customer': customer,
            'customer_reqs': customer_reqs,
            'customer_kw_total': sum(kwList),
            'payment_list': payment_list,
            'payment_sum': payment_sum,
            'totalRes': totalRes,
            'pay_sum': paySum,
            'req_count': request_count
        }
        return response

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CustomerRequestsListView, self).get_context_data(**kwargs)
        return context


class CustomerRequestDetailsView(DetailView):
    template_name = 'requests/fbv/details.html'
    model = Requests
    # context_object_name = 'request'

    def dispatch(self, request, *args, **kwargs):
        req = self.get_object()
        # print(req.customer.user.last_name)
        if request.user != req.customer.user:
            messages.error(request, 'مجاز نیستید.')
            return redirect('errorpage')
        return super(CustomerRequestDetailsView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CustomerRequestDetailsView, self).get_context_data(**kwargs)
        request = self.request
        request_pk = self.kwargs.get("pk")
        req = Requests.objects.filter(is_active=True).get(pk=request_pk)
        # colleagues = req.colleagues.all()
        # colleague = False
        # if request.user in colleagues:
        #     colleague = True

        reqspecs = req.reqspec_set.all()
        req_files = req.requestfiles_set.all()
        nested_files = nd.nested_dict()
        req_imgs = []
        req_pdfs = []
        req_words = []
        req_other_files = []
        files = {}

        xfiles = {
            'img': {},
            'pdf': {},
            'doc': {},
            'other': {},
        }

        for f in req_files:
            if str(f.image).lower().endswith('.jpg') or str(f.image).lower().endswith('.jpeg') or str(
                    f.image).lower().endswith('.png'):
                req_imgs.append(f)
                nested_files['ximg'][f.pk]['url'] = f.image.url
                nested_files['ximg'][f.pk]['name'] = f.image.name.split('/')[-1]
                # nested_files['img']['name'] = f.image.name.split('/')
                xfiles['img'][f.pk] = {}
                xfiles['img'][f.pk]['url'] = f.image.url
                xfiles['img'][f.pk]['name'] = f.image.name.split('/')[-1]
            elif str(f.image).lower().endswith('.pdf'):
                req_pdfs.append(f)
                nested_files['pdf']['url'] = f.image.url
                nested_files['pdf']['name'] = f.image.name.split('/')[-1]
                xfiles['pdf'][f.pk] = {}
                xfiles['pdf'][f.pk]['url'] = f.image.url
                xfiles['pdf'][f.pk]['name'] = f.image.name.split('/')[-1]

            elif str(f.image).lower().endswith('.doc'):
                req_words.append(f)
                xfiles['doc'][f.pk] = {}
                xfiles['doc'][f.pk]['url'] = f.image.url
                xfiles['doc'][f.pk]['name'] = f.image.name.split('/')[-1]
            else:
                req_other_files.append(f)
                xfiles['other'][f.pk] = {}
                xfiles['other'][f.pk]['url'] = f.image.url
                xfiles['other'][f.pk]['name'] = f.image.name.split('/')[-1]

        files['req_imgs'] = req_imgs
        files['req_pdfs'] = req_pdfs
        files['req_words'] = req_words
        files['req_other_files'] = req_other_files

        img_names = {}
        for r in req_files:
            name = r.image.name
            newname = name.split('/')
            las = newname[-1]
            img_names[r.pk] = las

        # for x, y in nested_files['ximg'].items():
        #     print(f"last is: {y['name']}")

        kw = total_kw(request_pk)
        respone = {
            'req': req,
            'reqspecs': reqspecs,
            'req_images': req_files,
            'total_kw': kw,
            'files': files,
            'nested_files': nested_files,
            'xfiles': xfiles
        }
        # context["response"] = respone
        context.update(respone)
        return context


class CustomerCreateRequestview(CreateView):
    template_name = 'requests/fbv/req_form.html'
    form_class = CustomerRequestCreateForm

    # def form_valid(self, form):
    #     if self.request == 'POST'


class CustomerReqSpecCreateView(CreateView):
    template_name = 'requests/fbv/spec_form.html'
    form_class = SpecForm

