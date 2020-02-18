import json

from graphene_django.utils.testing import GraphQLTestCase

from accounts.tests.test_public_funcs import CustomAPITestCase
from factor.schema import schema


class TypeTestCase(GraphQLTestCase, CustomAPITestCase):
    GRAPHQL_SCHEMA = schema

    def test_some_query(self):
        """Test retrieve customers list """
        query = '''
            query{
              allCustomers {
                edges {
                  node {
                    id
                    name
                  }
                }
              }
            }
            '''
        response = self.query(query)
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertEqual(len(content['data']['allCustomers']['edges']), 1)
        self.assertEqual(content['data']['allCustomers']['edges'][0]['node']['name'], 'zsamplecustomer')
        # result = schema.execute(query)
        # assert not result.errors

    def test_retreive_customer_by_id(self):
        """Test retrieve customer by id"""
        query = """
            {
              customer(id:"Q3VzdG9tZXJOb2RlOjE=") {
                id
                name
              }
            }
        """
        response = self.query(query)
        json_response = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertEqual(json_response['data']['customer']['id'], "Q3VzdG9tZXJOb2RlOjE=")
        self.assertEqual(json_response['data']['customer']['name'], "zsamplecustomer")

    def test_retreive_customer_by_id_as_variable(self):
        """Test retrieve customer by id passed as a variable"""
        query = """
            query customer($id: ID!){
              customer(id: $id) {
                id
                name
              }
            }
        """
        response = self.query(query, variables={'id': "Q3VzdG9tZXJOb2RlOjE="})
        json_response = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertEqual(json_response['data']['customer']['id'], "Q3VzdG9tZXJOb2RlOjE=")
        self.assertEqual(json_response['data']['customer']['name'], "zsamplecustomer")

    def test_filter_customers_by_name_icontains(self):
        """Test filter customers list by name icontains"""
        query = '''
            {
              allCustomers(name_Icontains:"zsamplec") {
                edges {
                  node {
                    id
                    name
                  }
                }
              }
            }
        '''
        response = self.query(query)
        json_reponse = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertEqual(len(json_reponse['data']['allCustomers']['edges']), 1)
        self.assertEqual(json_reponse['data']['allCustomers']['edges'][0]['node']['id'], "Q3VzdG9tZXJOb2RlOjE=")
        self.assertEqual(json_reponse['data']['allCustomers']['edges'][0]['node']['name'], "zsamplecustomer")

    def test_filter_customers_by_name_exact(self):
        """Test filter customers list by exact name"""
        query = '''
            {
              allCustomers(name:"zsamplecustomer") {
                edges {
                  node {
                    id
                    name
                  }
                }
              }
            }
        '''
        response = self.query(query)
        json_reponse = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertEqual(len(json_reponse['data']['allCustomers']['edges']), 1)
        self.assertEqual(json_reponse['data']['allCustomers']['edges'][0]['node']['id'], "Q3VzdG9tZXJOb2RlOjE=")
        self.assertEqual(json_reponse['data']['allCustomers']['edges'][0]['node']['name'], "zsamplecustomer")
