import json
from graphene_django.utils.testing import GraphQLTestCase
from accounts.tests.test_public_funcs import CustomAPITestCase
from factor.schema import schema


class TestProforma(GraphQLTestCase, CustomAPITestCase):

    GRAPHQL_SCHEMA = schema

    def test_proforma_list(self):
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

        self.assertResponseNoErrors(response)
        self.assertEqual(len(proformas), 3)
        # todo: test sort orders...
        # self.assertEqual(proformas[0]['node']['id'], 'UHJvZm9ybWFOb2RlOjE=')
        # self.assertEqual(proformas[0]['node']['number'], 981000)

    def test_proforma_filter_by_customer_name(self):
        """Test proformas filter by customer name"""
        self.customer = self.sample_customer(owner=self.user, name='pars tehran')
        req = self.sample_request(owner=self.ex_user, customer=self.customer, number=981515)
        spec1 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=55, rpm=1000)
        spec2 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=315, rpm=1500)
        spec3 = self.sample_reqspec(owner=self.ex_user, req_id=req, kw=160, rpm=3000)
        self.proforma_payload.update({'req_id': req.pk})
        proforma = self.sample_proforma(req=req, owner=self.ex_user, number=15325)
        query = '''
            query{
              allProformas(reqId_Customer_Name_Icontains:"zsamp") {
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
        response = self.query(query)
        json_response = json.loads(response.content)
        proformas = json_response['data']['allProformas']['edges']

        self.assertResponseNoErrors(response)
        self.assertEqual(len(proformas), 1)

    def test_retrieve_proforma_by_number(self):
        """Test Retrieve Proforma By Number"""
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

    def test_retrieve_proforma_by_id(self):
        self.assertTrue(False)

    def test_retrieve_proforma_by_id_not_found(self):
        self.assertTrue(False)
