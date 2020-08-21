import json
from graphene_django.utils.testing import GraphQLTestCase
from accounts.tests.test_public_funcs import CustomAPITestCase
from factor.schema import schema

# Create your tests here.


class TestIncomes(GraphQLTestCase, CustomAPITestCase):
    GRAPHQL_SCHEMA = schema

    # Queries
    def test_retrieve_income_list(self):
        """Test retreive income list"""

        self.sample_income_new(number=123654)
        self.sample_income_new(number=154)
        self.sample_income_new(number=987)
        query = '''
            {
              allIncomes {
                edges {
                  node {
                    number
                    amount
                  }
                }
              }
            }
        '''
        response = self.query(query)
        json_response = json.loads(response.content)

        incomes = json_response['data']['allIncomes']['edges']
        self.assertTrue('data' in json_response)
        self.assertEqual(len(incomes), 4)
        self.assertEqual(incomes[0]['node']['number'], 9807)

    def test_retrieve_incomes_by_customer(self):
        """Test retrieve incomes by customer"""
        new_customer = self.sample_customer(owner=self.user, name='temp_customer')
        self.sample_income_new(customer=new_customer, number=6548)
        self.sample_income_new(customer=new_customer, number=123654)
        self.sample_income_new(number=154)
        self.sample_income_new(number=987)

        query = '''
            query($name:String){
              allIncomes(customer_Name_Icontains:$name) {
                edges {
                  node {
                    number
                    amount
                    customer{
                      name
                    }
                  }
                }
              }
            }
            '''
        response = self.query(query, variables={
            'name': new_customer.name
        })
        json_response = json.loads(response.content)
        incomes = json_response['data']['allIncomes']['edges']
        self.assertTrue('data' in json_response)
        self.assertEqual(len(incomes), 2)
        self.assertEqual(incomes[0]['node']['number'], 6548)

    def test_retrieve_incomes_by_date(self):
        """Test retrieve incomes by date"""
        pass

    def test_retrieve_incomes_by_type(self):
        """Test retrieve incomes by type"""
        pass

    def test_retrieve_incomes_by_owner(self):
        """Test retrieve incomes by owner"""
        new_customer = self.sample_customer(owner=self.user, name='temp_customer')
        self.sample_income_new(owner=self.ex_user, customer=new_customer, number=6548)
        self.sample_income_new(owner=self.ex_user, customer=new_customer, number=123654)
        self.sample_income_new(owner=self.ex_user, number=154)
        self.sample_income_new(owner=self.user, number=987)
        self.user.last_name = 'someLastName'
        self.user.save()

        query = '''
            query($name:String){
                allIncomes(owner_LastName_Icontains:$name) {
                  edges {
                    node {
                      number
                      amount
                      customer{
                        name
                      }
                      owner{
                        username
                      }
                    }
                  }
                }
              }
        '''
        response = self.query(query, variables={
            'name': self.user.last_name
        })
        json_response = json.loads(response.content)

        incomes = json_response['data']['allIncomes']['edges']
        self.assertTrue('data' in json_response)
        self.assertEqual(len(incomes), 1)
        self.assertEqual(incomes[0]['node']['number'], 987)

    def test_retrieve_incomes_by_due_date(self):
        """Test retrieve incomes by due_date"""
        pass

    def test_retrieve_income_by_id(self):
        """Test retrieve income by ID"""
        pass

    # Mutation
    def test_income_mutation_needs_permission(self):
        """Test income mutation needs permission"""
        mutation = '''
            mutation incomeMutation(
                $owner: ID!
                $customer: ID!
            ){
              incomeMutation(input:{
                owner: $owner
                customer: $customer
                number:321560
                amount:125000000
                dateFa:"1398-12-02"
                isActive:true
              }){
                income{
                  amount
                  number
                  amountAssigned
                }
                errors{
                  field
                  messages
                }
              }
            }
        '''
        response = self.query(mutation,
                              variables={
                                  'owner': self.user.pk,
                                  'customer': self.customer.pk
                              })
        json_response = json.loads(response.content)

        self.assertIsNone(json_response['data']['incomeMutation'])
        self.assertEqual(json_response['errors'][0]['message'], 'No permission to do that.')

    def test_income_mutation_success(self):
        """Test income mutation with success"""
        mutation = '''
            mutation incomeMutation(
                $owner: ID!
                $customer: ID!
            ){
              incomeMutation(input:{
                owner: $owner
                customer: $customer
                number:321560
                amount:125000000
                dateFa:"1398-12-02"
                isActive:true
              }){
                income{
                  amount
                  number
                  amountAssigned
                }
                errors{
                  field
                  messages
                }
              }
            }
        '''
        response = self.query(mutation,
                              variables={
                                  'owner': self.ex_user.pk,
                                  'customer': self.customer.pk
                              })
        json_response = json.loads(response.content)
        self.assertTrue('data' in json_response)
        self.assertEqual(json_response['data']['incomeMutation']['income']['number'], 321560)
        self.assertEqual(json_response['data']['incomeMutation']['income']['amount'], 125000000)

    def test_income_mutation_no_owner_fail(self):
        """Test income mutation fails if no owner provided????"""
        pass

    def test_income_mutation_no_customer_fail(self):
        """Test income mutation fails if no customer provided.????"""
        pass

    def test_income_mutation_no_amount_fails(self):
        """Test income mutation fails where no amount provided.????"""
        pass
