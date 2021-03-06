import json
import datetime
from graphql_relay import to_global_id
from graphql_jwt.testcases import JSONWebTokenTestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from customer.models import Type, Customer
from incomes.models import Income, IncomeRow
from motordb.models import MotorsCode
from request.models import *

User = get_user_model()


class JwtApi(JSONWebTokenTestCase):

    def setUp(self):
        self.user = self.sample_user(username='user')

        self.superuser = self.sample_superuser(username='superuser')
        self.sale_expert_group = Group.objects.create(name='sale_expert')
        self.ex_user = self.sample_expert_user(username='ex_user')

        self.customer_type = self.sample_customer_type()
        self.project_type = ProjectType.objects.create(title='روتین')
        self.im = IMType.objects.create(title='IMB3')
        self.ip = IPType.objects.create(title='IP55')
        self.ic = ICType.objects.create(title='IC411')
        self.ie = IEType.objects.create(title='IE1')
        self.rpm_new = RpmType.objects.create(rpm='1500', pole='4')
        self.code = 99009900

        self.customer = self.sample_customer(owner=self.user, name='zsamplecustomer')
        self.req = self.sample_request(owner=self.user, customer=self.customer, number=981010)

        self.spec1 = self.sample_reqspec(owner=self.user, kw=55, rpm=1000)
        self.spec2 = self.sample_reqspec(owner=self.user, kw=315, rpm=1500)
        self.spec3 = self.sample_reqspec(owner=self.user, kw=160, rpm=3000)
        self.proforma = self.sample_proforma(req=self.req, owner=self.user, number=981000)
        self.payment = self.sample_payment(proforma=self.proforma, owner=self.user, number=45422345, amount=84532135100)
        self.motorcode = self.sample_motorcode(owner=self.user, code=9900, kw=450, speed=1500, voltage=380)

        self.income = self.sample_income_new(number=9807)
        self.income_row = self.sample_income_row()
        self.request_payload = {
            'number': 1000,
            'customer': self.customer.pk,
            "date_fa": "1398-05-06",
        }
        self.reqspec_payload = {
            'req_id': self.req.pk,
            'code': self.code,
            'qty': 3,
            'kw': 315,
            'rpm_new': self.rpm_new.pk,
            'voltage': 380,
            'im': self.im.pk,
            'ip': self.ip.pk,
            'ic': self.ic.pk,
            'ie': self.ie.pk,
            'type': self.project_type.pk,
        }
        self.motorcode_payload = {
            'code': self.code,
            'qty': 3,
            'kw': 315,
            'speed': self.rpm_new.pk,
            'voltage': 380,
            'im': self.im.pk,
            'ip': self.ip.pk,
            'ic': self.ic.pk,
            'ie': self.ie.pk,
            'type': self.project_type.pk,
        }
        self.proforma_payload = {
            'req_id': self.req.pk,
            'date_fa': ['۱۳۹۸-۰۶-۰۳'],
            'exp_date_fa': ['۱۳۹۸-۰۶-۰۳'],
            'summary': ['somte data goes here...'],
        }

        self.payment_payload = {
            'xpref_id': self.proforma.pk,
            'number': 15220,
            'amount': 1500000,
            'date_fa': '۱۳۹۸-۰۶-۰۳',
            # 'date_fa': ['۱۳۹۸-۰۶-۰۳'],
            'summary': 'somte data goes here...',
            # 'summary': ['somte data goes here...'],
        }
        self.prefspec_payload = {}

    def sample_user(self, username='testuser', password='testpass123'):
        """Create a sample user"""
        return User.objects.create_user(username, password)

    def sample_superuser(self, username='superuser'):
        user = self.sample_user(username=username)
        user.is_superuser = True
        user.save()
        return user

    def sample_customer_type(self, name='پتروشیمی'):
        """Create a sample customer type"""
        return Type.objects.create(name=name)

    def sample_customer(
            self, date2=datetime.datetime.now(), **params
    ):
        defaults = {
            'owner': self.user,
            'type': self.customer_type,
        }
        defaults.update(params)
        customer = Customer.objects.create(
            date2=date2,
            **defaults
        )
        return customer

    def sample_request(self, **params):
        # if not owner:
        #     owner = self.sample_user()
        # if customer is None:
        #     customer = self.sample_customer()
        defaults = {
            'owner': self.user,
            'customer': self.customer,
        }
        defaults.update(params)
        req = Requests.objects.create(
            **defaults
        )
        return req

    def sample_expert_user(self, username='expert_user'):
        ex_user = self.sample_user(username=username)
        ex_user.groups.add(self.sale_expert_group)
        self.sale_expert_group.permissions.add(
            Permission.objects.get(codename='add_customer', content_type__app_label='customer'),
            Permission.objects.get(codename='index_customer', content_type__app_label='customer'),
            Permission.objects.get(codename='read_customer', content_type__app_label='customer'),
            Permission.objects.get(codename='change_customer', content_type__app_label='customer'),
            Permission.objects.get(codename='delete_customer', content_type__app_label='customer'),
            Permission.objects.get(codename='index_requests', content_type__app_label='request'),
            Permission.objects.get(codename='read_requests', content_type__app_label='request'),
            Permission.objects.get(codename='add_requests', content_type__app_label='request'),
            Permission.objects.get(codename='delete_requests', content_type__app_label='request'),
            Permission.objects.get(codename='change_requests', content_type__app_label='request'),
            Permission.objects.get(codename='add_reqspec', content_type__app_label='request'),
            Permission.objects.get(codename='index_reqspecs', content_type__app_label='request'),
            Permission.objects.get(codename='index_reqspec', content_type__app_label='request'),
            Permission.objects.get(codename='change_reqspec', content_type__app_label='request'),
            Permission.objects.get(codename='delete_reqspec', content_type__app_label='request'),
            Permission.objects.get(codename='read_reqspecs', content_type__app_label='request'),
            Permission.objects.get(codename='add_reqpart', content_type__app_label='request'),
            Permission.objects.get(codename='change_reqpart', content_type__app_label='request'),
            # works with rest_framework
            Permission.objects.get(codename='index_xpref', content_type__app_label='request'),
            # works with fbv
            Permission.objects.get(codename='index_proforma', content_type__app_label='request'),
            Permission.objects.get(codename='read_proforma', content_type__app_label='request'),
            Permission.objects.get(codename='add_xpref', content_type__app_label='request'),
            Permission.objects.get(codename='delete_xpref', content_type__app_label='request'),
            Permission.objects.get(codename='change_xpref', content_type__app_label='request'),
            Permission.objects.get(codename='index_prefspec', content_type__app_label='request'),
            Permission.objects.get(codename='add_prefspec', content_type__app_label='request'),
            Permission.objects.get(codename='delete_prefspec', content_type__app_label='request'),
            Permission.objects.get(codename='change_prefspec', content_type__app_label='request'),
            Permission.objects.get(codename='index_payment', content_type__app_label='request'),
            Permission.objects.get(codename='add_payment', content_type__app_label='request'),
            Permission.objects.get(codename='change_payment', content_type__app_label='request'),
            Permission.objects.get(codename='read_payment', content_type__app_label='request'),
            Permission.objects.get(codename='delete_payment', content_type__app_label='request'),
            Permission.objects.get(codename='add_income', content_type__app_label='incomes'),
            # Permission.objects.get(codename='index_income', content_type__app_label='incomes'),
            Permission.objects.get(codename='change_income', content_type__app_label='incomes'),
            # Permission.objects.get(codename='read_income', content_type__app_label='incomes'),
            Permission.objects.get(codename='delete_income', content_type__app_label='incomes'),
            Permission.objects.get(codename='add_incomerow', content_type__app_label='incomes'),
            # Permission.objects.get(codename='index_incomerow', content_type__app_label='incomes'),
            Permission.objects.get(codename='change_incomerow', content_type__app_label='incomes'),
            # Permission.objects.get(codename='read_incomerow', content_type__app_label='incomes'),
            Permission.objects.get(codename='delete_incomerow', content_type__app_label='incomes'),
            Permission.objects.get(codename='add_motorscode', content_type__app_label='motordb'),
            Permission.objects.get(codename='index_motorscode', content_type__app_label='motordb'),
            Permission.objects.get(codename='change_motorscode', content_type__app_label='motordb'),
            Permission.objects.get(codename='delete_motorscode', content_type__app_label='motordb'),
        )
        ex_user.super_user = True
        ex_user.save()
        return ex_user

    def sample_reqspec(self, **params):
        defaults = {
            'req_id': self.req,
            'type': self.project_type,
            'rpm_new': RpmType.objects.create(rpm=1500, pole=4),
            'qty': 2, 'kw': 132, 'rpm': 1500, 'voltage': 380,
        }
        defaults.update(params)

        return ReqSpec.objects.create(**defaults)

    def sample_reqpart(self, **params):
        defaults = {
            'owner': self.user,
            'req': self.req,
            'qty': 2,
            'title': 'درپوش عایقی',
        }
        defaults.update(params)

        return ReqPart.objects.create(**defaults)

    def sample_proforma(self, req, owner, number, **params):
        defaults = {}
        defaults.update(params)
        return Xpref.objects.create(req_id=req, owner=owner, number=number, **defaults)

    def sample_payment(self, proforma, owner, number, amount, **params):
        defaults = {}
        defaults.update(params)
        return Payment.objects.create(xpref_id=proforma, owner=owner, number=number, amount=amount, **defaults)

    def sample_prefspec(self, proforma, owner, reqspe, **params):
        defaults = {
            'kw': reqspe.kw,
            'rpm': reqspe.rpm,
            'price': 1000
        }
        defaults.update(params)
        return PrefSpec.objects.create(xpref_id=proforma, owner=owner, reqspec_eq=reqspe, **defaults)

    def sample_income(self, **params):
        defaults = {
            'amount': 1500000,
        }
        defaults.update(params)
        return Payment.objects.create(**defaults)

    def sample_motorcode(self, **params):
        im = IMType.objects.create(title='IMB35')
        ip = IPType.objects.create(title='IP56')
        ic = ICType.objects.create(title='IC511')
        ie = IEType.objects.create(title='IE2')
        default = {
            'ie': ie.title,
            'im': im.title,
            'ic': ic.title,
            'ip': ip.title,
        }
        default.update(params)
        return MotorsCode.objects.create(**default)

    def sample_income_new(self, **params):
        default = {
            'owner': self.ex_user,
            'customer': self.customer,
            'amount': 25600000,
            'date_fa': "1398-02-03",
            'summary': "for test purposes",
            'is_active': True,
        }
        default.update(params)
        income = Income.objects.create(**default)

        return income

    def sample_income_row(self, **params):
        default = {
            'owner': self.ex_user,
            'income': self.income,
            'proforma': self.proforma,
            'amount': 25600,
            'date_fa': "1398-02-03",
            'summary': "for test purposes",
            'is_active': True,
        }
        default.update(params)
        income_row = IncomeRow.objects.create(**default)

        return income_row


class TestOrders(JwtApi):

    def test_request_mutation_success2(self):
        """Test request mutation success"""
        self.client.authenticate(self.ex_user)

        mutation = '''
            mutation ReqMutation(
                $customer: ID!
                $owner: ID!
                $colleague: [ID]
            ){
              requestMutation(input:{
                customer: $customer
                owner:$owner
                clientMutationId:"klsjf"
                number:18665
                colleagues:$colleague
                dateFa: "1398-02-12"
                summary: "something about this request"
              }){
                requests{
                  id
                  number
                  owner{
                    id
                    username
                  }
                  customer{
                    name
                  }
                }
                errors{
                field,
                  messages
              }
              }
            }
        '''
        variables = {
            'customer': to_global_id('CustomerNode', self.customer.pk),
            'owner': '',
            'colleague': []
        }

        response = self.client.execute(mutation, variables)
        self.assertTrue(hasattr(response, 'data') and response.data['requestMutation']['requests'] is not None)

        self.assertEqual(response.data['requestMutation']['requests']['number'], 18665)
        self.assertEqual(response.data['requestMutation']['requests']['customer']['name'], 'zsamplecustomer')
        self.assertEqual(response.data['requestMutation']['requests']['owner']['username'], self.ex_user.username)

    # def test_request_mutation_no_customer_fail(self):
    #     """Test request mutation fails with no customer"""
    #     self.client.authenticate(self.ex_user)
    #     mutation = '''
    #                 mutation ReqMutation(
    #                     $customer: ID!
    #                     $owner: ID!
    #                     $colleague: [ID]
    #                 ){
    #                   requestMutation(input:{
    #                     owner:$owner
    #                     customer:$customer
    #                     clientMutationId:"klsjf"
    #                     number:18665
    #                     colleagues:$colleague
    #                     dateFa: "1398-02-12"
    #                     summary: "something about this request"
    #                   }){
    #                     requests{
    #                       id
    #                       number
    #                       customer{
    #                         name
    #                       }
    #                     }
    #                     errors{
    #                     field,
    #                       messages
    #                   }
    #                   }
    #                 }
    #             '''
    #     variables = {
    #         'owner': '',
    #         'colleague': [to_global_id('UserNode', self.user.pk)],
    #         'customer': ''
    #     }
    #     response = self.client.execute(mutation, variables)
    #     # self.assertIsNone(response.data['requestMutation'])
    #     self.assertTrue(hasattr(response, 'data') and response.data['requestMutation'] is None)

    def test_request_mutation_number_exists_fail(self):
        """Test request mutation fails when number exists"""
        self.client.authenticate(self.ex_user)
        req = self.sample_request(owner=self.ex_user, customer=self.customer, number=981515)

        mutation = '''
            mutation ReqMutation(
                $customer: ID!
                $owner: ID!
                $colleague: [ID]
                $number: Int!
            ){
              requestMutation(input:{
                owner:$owner
                customer: $customer
                clientMutationId:"klsjf"
                number:$number
                colleagues:$colleague
                dateFa: "1398-02-12"
                summary: "something about this request"
              }){
                requests{
                  id
                  number
                  customer{
                    name
                  }
                }
                errors{
                field,
                  messages
              }
              }
            }
        '''
        variables = {
            'owner': '',
            'customer': to_global_id('CustomerNode', self.customer.pk),
            'colleague': [],
            'number': req.number
        }
        response = self.client.execute(mutation, variables)
        self.assertTrue(hasattr(response, 'data') and response.data['requestMutation']['errors'] is not None)

    def test_reqspec_mutation_success(self):
        self.client.authenticate(self.ex_user)
        req = self.sample_request(owner=self.ex_user, customer=self.customer, number=981515)
        mutation = '''
            mutation reqSpecMutation(
                $reqId: ID!
                $owner: ID!
                $type: ID!
                $rpm_new: ID!
            ){
              reqSpecMutation(input:{
                clientMutationId:"alsdjf"
                code:99009900
                reqId:$reqId
                owner:$owner
                qty:25
                kw:132
                rpm:1500
                voltage:380
                rpmNew:$rpm_new
                type:$type
              }){
                reqSpec{
                  qty
                  kw
                  rpm
                  voltage
                }
                errors{
                  field,
                  messages
                }
              }
            }
        '''
        variables = {
            'reqId': to_global_id('RequestNode', req.pk),
            'owner': '',
            'type': self.project_type.pk,
            'rpm_new': to_global_id('RpmTypeNode', self.rpm_new.pk)
        }
        response = self.client.execute(mutation, variables)
        reqspec = req.reqspec_set.last()
        self.assertEqual(reqspec.kw, response.data['reqSpecMutation']['reqSpec']['kw'])
        self.assertEqual(reqspec.rpm, response.data['reqSpecMutation']['reqSpec']['rpm'])
        self.assertEqual(reqspec.voltage, response.data['reqSpecMutation']['reqSpec']['voltage'])
        self.assertEqual(reqspec.qty, response.data['reqSpecMutation']['reqSpec']['qty'])

