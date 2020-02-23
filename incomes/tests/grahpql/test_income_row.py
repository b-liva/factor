import json
from graphene_django.utils.testing import GraphQLTestCase
from accounts.tests.test_public_funcs import CustomAPITestCase
from factor.schema import schema

# Create your tests here.


class TestIncomes(GraphQLTestCase, CustomAPITestCase):
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        super().setUp()
        self.specs_payload = [
            {'qty': 132, 'kw': 132, 'rpm': 1500, 'voltage': 380},
            {'qty': 315, 'kw': 160, 'rpm': 1500, 'voltage': 380},
            {'qty': 132, 'kw': 315, 'rpm': 3000, 'voltage': 380},
            {'qty': 75, 'kw': 75, 'rpm': 1000, 'voltage': 380},
        ]

    # Queries
    def test_retrieve_income_rows_list(self):
        """Test retreive income_rows list"""

        income_rows1 = self.sample_income_row()
        income_rows2 = self.sample_income_row()
        income_rows3 = self.sample_income_row()
        query = '''
            {
              allIncomeRows {
                edges {
                  node {
                    amount
                  }
                }
              }
            }
        '''
        response = self.query(query)
        json_response = json.loads(response.content)
        income_rows = json_response['data']['allIncomeRows']['edges']
        self.assertTrue('data' in json_response)
        self.assertEqual(len(income_rows), 4)
        self.assertEqual(income_rows[0]['node']['amount'], 25600)

    def test_retrieve_income_rows_by_date(self):
        """Test retrieve income_rows by date"""
        pass

    def test_retrieve_income_rows_by_owner(self):
        """Test retrieve income_rows by owner"""
        pass

    def test_retrieve_income_rows_by_customer(self):
        """Test retrieve income_rows by customer"""
        pass

    # Mutation
    def test_income_rows_mutation_needs_permission(self):
        """Test income row mutation needs permission."""
        mutation = '''
            mutation incomeRowMutation(
              $owner:ID!
              $income: ID!
              $proforma:ID!
            ){
              incomeRowMutation(input:{
                owner:$owner
                income:$income
                proforma:$proforma
                amount:4550000
                dateFa: "1398-02-03"
              }){
                incomeRow{
                  id
                  amount
                }
                errors{
                  field
                  messages
                }
              }
            }
            '''
        response = self.query(mutation, variables={
            'owner': self.user.pk,
            'proforma': self.proforma.pk,
            'income': self.income.pk
        })
        json_response = json.loads(response.content)

        self.assertIsNone(json_response['data']['incomeRowMutation'])

        self.assertEqual(json_response['errors'][0]['message'], 'No permission to do that.')

    def test_income_rows_mutation_success(self):
        """Test income_rows mutation with success"""
        spec1 = self.sample_reqspec(req_id=self.req, owner=self.ex_user, **self.specs_payload[0])
        spec2 = self.sample_reqspec(req_id=self.req, owner=self.ex_user, **self.specs_payload[1])

        prefspec1 = self.sample_prefspec(proforma=self.proforma, owner=self.ex_user, reqspe=spec1, price=12350000)
        prefspec2 = self.sample_prefspec(proforma=self.proforma, owner=self.ex_user, reqspe=spec2, price=25000000)

        mutation = '''
            mutation incomeRowMutation(
              $owner:ID!
              $income: ID!
              $proforma:ID!
            ){
              incomeRowMutation(input:{
                owner:$owner
                income:$income
                proforma:$proforma
                amount:4550000
                dateFa: "1398-02-03"
              }){
                incomeRow{
                  id
                  amount
                }
                errors{
                  field
                  messages
                }
              }
            }
        '''
        response = self.query(mutation, variables={
            'owner': self.ex_user.pk,
            'proforma': self.proforma.pk,
            'income': self.income.pk
        })
        json_response = json.loads(response.content)

        self.assertTrue('data' in json_response)
        self.assertEqual(json_response['data']['incomeRowMutation']['incomeRow']['amount'], 4550000)

    def test_income_row_mutation_fails_if_sum_gt_income_amount(self):
        """Test income row mutation fails if sum of income rows of the related income is greater than income amount"""
        req = self.sample_request(owner=self.ex_user, customer=self.customer, number=982020)
        spec1 = self.sample_reqspec(req_id=req, owner=self.ex_user, **self.specs_payload[0])
        spec2 = self.sample_reqspec(req_id=req, owner=self.ex_user, **self.specs_payload[1])
        prof = self.sample_proforma(req=req, number=984040, owner=self.ex_user)

        prefspec1 = self.sample_prefspec(proforma=prof, owner=self.ex_user, reqspe=spec1, price=12350000)
        prefspec2 = self.sample_prefspec(proforma=prof, owner=self.ex_user, reqspe=spec2, price=25000000)

        income = self.sample_income_new(number=9809, amount=20000000)

        income_rows1 = self.sample_income_row(income=income, proforma=prof, amount=10000000)
        income_rows2 = self.sample_income_row(income=income, proforma=prof, amount=2000000)
        income_rows3 = self.sample_income_row(income=income, proforma=prof, amount=3000000)

        mutation = '''
            mutation incomeRowMutation(
              $owner:ID!
              $income: ID!
              $proforma:ID!
            ){
              incomeRowMutation(input:{
                owner:$owner
                income:$income
                proforma:$proforma
                amount:6000000
                dateFa: "1398-02-03"
              }){
                incomeRow{
                  id
                  amount
                }
                errors{
                  field
                  messages
                }
              }
            }
            '''
        response = self.query(mutation, variables={
            'owner': self.ex_user.pk,
            'proforma': prof.pk,
            'income': income.pk
        })

        # print(f'proforma vat: {prof.number}', prof.total_proforma_price_vat()['price_vat'])
        json_response = json.loads(response.content)
        # TODO: proper error message.
        self.assertIsNone(json_response['data']['incomeRowMutation'])

    def test_income_row_mutation_fails_if_sum_gt_proforma_amount(self):
        """Test income row mutation fails if sum of income rows of the related income is greater than proforma amount"""
        req = self.sample_request(owner=self.ex_user, customer=self.customer, number=982020)
        spec1 = self.sample_reqspec(req_id=req, owner=self.ex_user, **self.specs_payload[0])
        spec2 = self.sample_reqspec(req_id=req, owner=self.ex_user, **self.specs_payload[1])
        prof = self.sample_proforma(req=req, number=984040, owner=self.ex_user)

        prefspec1 = self.sample_prefspec(proforma=prof, owner=self.ex_user, reqspe=spec1, price=1235000)
        prefspec2 = self.sample_prefspec(proforma=prof, owner=self.ex_user, reqspe=spec2, price=2500000)

        income = self.sample_income_new(number=9809, amount=20355750)

        income_rows1 = self.sample_income_row(income=income, proforma=prof, amount=2035750)

        mutation = '''
            mutation incomeRowMutation(
              $owner:ID!
              $income: ID!
              $proforma:ID!
            ){
              incomeRowMutation(input:{
                owner:$owner
                income:$income
                proforma:$proforma
                amount:18000000
                dateFa: "1398-02-03"
              }){
                incomeRow{
                  id
                  amount
                }
                errors{
                  field
                  messages
                }
              }
            }
            '''
        response = self.query(mutation, variables={
            'owner': self.ex_user.pk,
            'proforma': prof.pk,
            'income': income.pk
        })

        # print(f'proforma vat: {prof.number}', prof.total_proforma_price_vat()['price_vat'])
        json_response = json.loads(response.content)
        # TODO: proper error message.
        self.assertIsNone(json_response['data']['incomeRowMutation'])

    def test_income_row_mutation_fails_if_date_is_prior_to_proforma_date(self):
        """Test income row mutation fails if date is prior to proforma date."""
        pass

    def test_income_rows_mutation_no_owner_fail(self):
        """Test income_rows mutation fails if no owner provided????"""
        pass

    def test_income_rows_mutation_no_customer_fail(self):
        """Test income_rows mutation fails if no customer provided.????"""
        pass

    def test_income_rows_mutation_no_amount_fails(self):
        """Test income_rows mutation fails where no amount provided.????"""
        pass

    def test_income_row_mutation_fails_if_owner_mismatch(self):
        """Test income row can't be saved if the current user is not the income owner"""
        pass

    def test_income_row_mutation_fails_if_customer_mismatch(self):
        """Test income row can't be saved if the proforma customer is not the income customer"""
        new_customer = self.sample_customer(owner=self.user, name='temp_customer')
        new_income = self.sample_income_new(customer=new_customer, number=6548)
        mutation = '''
            mutation incomeRowMutation(
              $owner:ID!
              $income: ID!
              $proforma:ID!
            ){
              incomeRowMutation(input:{
                owner:$owner
                income:$income
                proforma:$proforma
                amount:4550000
                dateFa: "1398-02-03"
              }){
                incomeRow{
                  id
                  amount
                }
                errors{
                  field
                  messages
                }
              }
            }
                    '''
        response = self.query(mutation, variables={
            'owner': self.ex_user.pk,
            'proforma': self.proforma.pk,
            'income': new_income.pk
        })
        json_response = json.loads(response.content)
        self.assertIsNone(json_response['data']['incomeRowMutation'])
        self.assertEqual(json_response['errors'][0]['message'], 'customer mismatch')
