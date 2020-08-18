import json
from graphene_django.utils.testing import GraphQLTestCase
from graphql_relay import to_global_id

from accounts.tests.test_public_funcs import CustomAPITestCase, Xpref
from factor.schema import schema


class TestProforma(GraphQLTestCase, CustomAPITestCase):

    GRAPHQL_SCHEMA = schema

    def test_proforma_list(self):
        """Test owner can list own proformas"""

        self._client.force_login(user=self.ex_user)
        req = self.sample_request(owner=self.ex_user, customer=self.customer, number=981515)
        spec1 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=55, rpm=1000)
        spec2 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=315, rpm=1500)
        spec3 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=160, rpm=3000)
        self.proforma_payload.update({'req_id': req.pk})
        proforma = self.sample_proforma(req=req, owner=self.ex_user, number=15325)

        customer2 = self.customer = self.sample_customer(owner=self.user, name='pars tehran')
        req2 = self.sample_request(owner=self.ex_user, customer=customer2, number=982615)
        spec1 = self.sample_reqspec(owner=self.ex_user, req_id=req2, kw=55, rpm=1000)
        spec2 = self.sample_reqspec(owner=self.ex_user, req_id=req2, kw=315, rpm=1500)
        spec3 = self.sample_reqspec(owner=self.ex_user, req_id=req2, kw=160, rpm=3000)
        self.proforma_payload.update({'req_id': req2.pk})
        proforma2 = self.sample_proforma(req=req2, owner=self.ex_user, number=1654)

        query = '''
            query{
              allProformas {
                edges {
                  node {
                    id
                    number
                  }
                }
              }
            }
        '''
        response = self.query(query)
        json_response = json.loads(response.content)

        proformas = json_response['data']['allProformas']['edges']
        user_proformas = Xpref.objects.filter(owner=self.ex_user, is_active=True)
        self.assertResponseNoErrors(response)
        self.assertEqual(len(proformas), user_proformas.count())
        # todo: test sort orders...

    def test_proforma_filter_by_customer_name(self):
        """Test proformas filter by customer name"""
        self._client.force_login(user=self.ex_user)
        self.customer = self.sample_customer(owner=self.user, name='pars tehran')
        req = self.sample_request(owner=self.ex_user, customer=self.customer, number=981515)
        spec1 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=55, rpm=1000)
        spec2 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=315, rpm=1500)
        spec3 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=160, rpm=3000)
        self.proforma_payload.update({'req_id': req.pk})
        proforma = self.sample_proforma(req=req, owner=self.ex_user, number=15325)
        query = '''
            query xxx($customer_name:String){
              allProformas(reqId_Customer_Name_Icontains:$customer_name) {
                edges {
                  node {
                    id
                    number
                    customerName
                  }
                }
              }
            }

        '''
        variables = {
            "customer_name": req.customer.name
        }
        response = self.query(query, variables)
        json_response = json.loads(response.content)
        proformas = json_response['data']['allProformas']['edges']
        self.assertResponseNoErrors(response)
        self.assertEqual(len(proformas), 1)

    def test_retrieve_proforma_by_number(self):
        """Test Retrieve Proforma By Number"""
        self._client.force_login(user=self.ex_user)
        req = self.sample_request(owner=self.ex_user, customer=self.customer, number=981515)
        spec1 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=55, rpm=1000)
        spec2 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=315, rpm=1500)
        spec3 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=160, rpm=3000)
        self.proforma_payload.update({'req_id': req.pk})
        proforma = self.sample_proforma(req=req, owner=self.ex_user, number=15325)

        customer2 = self.customer = self.sample_customer(owner=self.user, name='pars tehran')
        req2 = self.sample_request(owner=self.ex_user, customer=customer2, number=982615)
        spec1 = self.sample_reqspec(owner=self.ex_user, req_id=req2, kw=55, rpm=1000)
        spec2 = self.sample_reqspec(owner=self.ex_user, req_id=req2, kw=315, rpm=1500)
        spec3 = self.sample_reqspec(owner=self.ex_user, req_id=req2, kw=160, rpm=3000)
        self.proforma_payload.update({'req_id': req2.pk})
        proforma = self.sample_proforma(req=req2, owner=self.ex_user, number=1654)

        query = '''
            query{
              allProformas(number:1654) {
                edges {
                  node {
                    id
                    number
                    customerName
                    reqId{
                      number
                      pubDate
                    }
                  }
                }
              }
            }
        '''
        response = self.query(query)
        json_response = json.loads(response.content)
        proformas = json_response['data']['allProformas']['edges']
        self.assertResponseNoErrors(response)
        self.assertEqual(len(proformas), 1)
        self.assertEqual(proformas[0]['node']['number'], 1654)

    def test_retrieve_proforma_by_number_not_found(self):
        self._client.force_login(user=self.ex_user)
        query = '''
            query{
              allProformas(number:1655) {
                edges {
                  node {
                    id
                    number
                    customerName
                    reqId{
                      number
                      pubDate
                    }
                  }
                }
              }
            }
                '''
        response = self.query(query)
        json_response = json.loads(response.content)
        proformas = json_response['data']['allProformas']['edges']
        self.assertResponseNoErrors(response)
        self.assertEqual(len(proformas), 0)

    def test_retrieve_proforma_by_id_needs_ownership(self):
        """Test owner can read own proformas"""
        self._client.force_login(user=self.user)
        query = '''
        query xxx($pid:ID!){
          proforma(id:$pid){
            id
            number
          }
        }
        '''
        variables = {
            "pid": to_global_id("ProformaNode", self.proforma.pk)
        }
        response = self.query(query, variables=variables)
        json_response = json.loads(response.content)
        self.assertResponseHasErrors(response)
        self.assertIsNone(json_response['data']['proforma'])

    def test_retrieve_proforma_by_id_not_found(self):
        self._client.force_login(user=self.ex_user)
        proforma_id = to_global_id("ProformaNode", self.proforma.pk)
        self.proforma.delete()
        query = '''
        query proforma($proforma_id:ID!){
          proforma(id:$proforma_id){
            id
            number
          }
        }
        '''
        variables = {
            "proforma_id": to_global_id("ProformaNode", proforma_id)
        }

        response = self.query(query, variables=variables)
        json_response = json.loads(response.content)
        print('Not Found: ', json_response)

        self.assertResponseHasErrors(response)
        self.assertIsNone(json_response['data']['proforma'])
