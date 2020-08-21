import datetime
import json
from graphene_django.utils.testing import GraphQLTestCase
from graphql_relay import from_global_id, to_global_id

from accounts.tests.test_public_funcs import CustomAPITestCase
from factor.schema import schema


class RequestTestCases(GraphQLTestCase, CustomAPITestCase):
    GRAPHQL_SCHEMA = schema

    # Queries and retrieval
    def date_time_converter(self, o):
        if isinstance(o, datetime.datetime):
            return o.__str__()

    def test_retrieve_payments_can_list_own(self):
        """Test retrieve list of own payments."""
        self._client.force_login(user=self.ex_user)
        payment = self.sample_payment(proforma=self.proforma, owner=self.ex_user, number=15345, amount=84532130000)
        query = '''
            {
              allPayments {
                edges {
                  node {
                    id
                    number
                    amount
                  }
                }
              }
            }
        '''
        response = self.query(query)
        response_json = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertEqual(len(response_json['data']['allPayments']['edges']), 1)
        self.assertEqual(response_json['data']['allPayments']['edges'][0]['node']['id'], to_global_id("PaymentNode", payment.pk))
        self.assertEqual(response_json['data']['allPayments']['edges'][0]['node']['number'], 15345)
        self.assertEqual(response_json['data']['allPayments']['edges'][0]['node']['amount'], 84532130000)

    def test_filter_payments_by_customer_name(self):
        """Test filter payments by customer name"""
        self._client.force_login(user=self.ex_user)
        payment = self.sample_payment(proforma=self.proforma, owner=self.ex_user, number=15345, amount=84532130000)
        query = '''
            {
              allPayments(xprefId_ReqId_Customer_Name_Icontains: "sampl") {
                edges {
                  node {
                    id
                    customerName
                    xprefId {
                      id
                      reqId {
                        id
                        customer {
                          id
                          name
                        }
                      }
                    }
                  }
                }
              }
            }
        '''
        response = self.query(query)
        json_response = json.loads(response.content)
        payments = json_response['data']['allPayments']['edges']
        self.assertResponseNoErrors(response)
        self.assertEqual(len(payments), 1)
        self.assertEqual(payments[0]['node']['customerName'], 'zsamplecustomer')
        self.assertEqual(from_global_id(payments[0]['node']['id'])[1], str(payment.pk))

    def test_retrieve_payment_by_id(self):
        """Test retrieve payment by id"""
        self._client.force_login(user=self.ex_user)
        payment = self.sample_payment(proforma=self.proforma, owner=self.ex_user, number=15345, amount=84532130000)

        query = '''
            query xxx($pid:ID!){
              payment(id:$pid) {
                id
                number
                amount
              }
            }
            '''
        variables = {
            'pid': to_global_id("PaymentNode", payment.pk)
        }
        response = self.query(query, variables=variables)
        json_response = json.loads(response.content)

        self.assertResponseNoErrors(response)
        self.assertEqual(json_response['data']['payment']['id'], to_global_id("PaymentNode", payment.pk))
        self.assertEqual(json_response['data']['payment']['number'], 15345)
        self.assertEqual(json_response['data']['payment']['amount'], 84532130000)

    def test_retrieve_payment_by_id_not_found(self):
        """Test retrieve payment by id not found"""
        query = '''
            query{
              payment(id:"UGF5bWVudE5vZGU6Mg==") {
                id
                number
                amount
              }
            }
            '''
        response = self.query(query)
        json_response = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertIsNone(json_response['data']['payment'])

    def test_retrieve_payment_by_number(self):
        self.assertTrue(False)

    def test_retrieve_payment_by_number_not_found(self):
        self.assertTrue(False)

    # Mutaions
    def test_payment_mutation_success(self):
        req = self.sample_request(owner=self.ex_user, customer=self.customer, number=981515)
        spec1 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=55, rpm=1000)
        spec2 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=315, rpm=1500)
        spec3 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=160, rpm=3000)
        self.proforma_payload.update({'req_id': req.pk})
        proforma = self.sample_proforma(req=req, owner=self.ex_user, number=15325)

        mutation = '''
            mutation paymentMutation(
                $owner: ID!
                $xprefId: ID!
                $pdate: DateTime!
            ){
              paymentMutation(input:{
                owner:$owner
                xprefId:$xprefId
                number:46485
                amount:13513510000
                paymentDate:$pdate
                dateFa:"1398-02-02"
              }){
                payment{
                  amount
                  xprefId{
                    number
                  }
                }
                errors{
                  field
                  messages
              }
              }
            }
        '''
        import datetime
        today = datetime.datetime.today()
        response = self.query(mutation, variables={
            'owner': proforma.owner.pk,
            'xprefId': proforma.pk,
            # 'pdate': json.dumps(today, default=self.date_time_converter)
            'pdate': "1992-10-09T00:00:00Z",
            # 'pdate': json.dumps(today, default=str) This also works.
        })
        json_respone = json.loads(response.content)

    # subscription
