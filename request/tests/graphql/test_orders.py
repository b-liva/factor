import json
from graphene_django.utils.testing import GraphQLTestCase
from graphql_relay import to_global_id
from accounts.tests.test_public_funcs import CustomAPITestCase
from factor.schema import schema


class TestReqeusts(GraphQLTestCase, CustomAPITestCase):

    GRAPHQL_SCHEMA = schema

    # query(retrieve)
    def test_request_list(self):
        pass

    def test_request_filter_by_customer_name(self):
        pass

    def test_retrieve_order_by_number(self):
        pass

    def test_retrieve_order_by_number_not_found(self):
        pass

    def test_retrieve_order_by_id(self):
        pass

    def test_retriev_order_by_id_not_found(self):
        pass

    # Mutations
    def test_request_mutation_success(self):
        """Test request mutation success"""
        self._client.force_login(user=self.ex_user)
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
            'customer': to_global_id("CustomerNode", self.customer.pk),
            'owner': "",
            'colleague': []
        }

        response = self.query(mutation, variables=variables)
        json_response = json.loads(response.content)

        self.assertResponseNoErrors(response)
        self.assertTrue('data' in json_response)
        self.assertIsNotNone(json_response['data']['requestMutation']['requests'])

        self.assertEqual(json_response['data']['requestMutation']['requests']['number'], 18665)
        self.assertEqual(json_response['data']['requestMutation']['requests']['customer']['name'], self.customer.name)

    def test_request_mutation_number_exists_fail(self):
        """Test request mutation fails when number exists"""
        self._client.force_login(user=self.ex_user)
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
                                customer:$customer
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
            'customer': to_global_id("CustomerNode", self.customer.pk),
            'colleague': [],
            'number': req.number
        }

        response = self.query(mutation, variables=variables)
        json_response = json.loads(response.content)

        self.assertNotEqual(json_response['data']['requestMutation']['errors'], [])
        self.assertTrue('number' in json_response['data']['requestMutation']['errors'][0].values())

    def test_request_mutation_future_date_fail(self):
        pass

    def test_reqspec_mutation_success(self):
        self._client.force_login(user=self.ex_user)
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
                  owner{
                    id
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
            'reqId': to_global_id("RequestNode", req.pk),
            'owner': "",
            'type': self.project_type.pk,
            'rpm_new': to_global_id("RpmTypeNode", self.rpm_new.pk)
        }
        response = self.query(mutation, variables=variables)
        json_response = json.loads(response.content)
        reqspec = req.reqspec_set.last()
        self.assertEqual(reqspec.kw, json_response['data']['reqSpecMutation']['reqSpec']['kw'])
        self.assertEqual(reqspec.rpm, json_response['data']['reqSpecMutation']['reqSpec']['rpm'])
        self.assertEqual(reqspec.voltage, json_response['data']['reqSpecMutation']['reqSpec']['voltage'])
        self.assertEqual(reqspec.qty, json_response['data']['reqSpecMutation']['reqSpec']['qty'])
        self.assertEqual(
            to_global_id("UserNode", reqspec.owner.pk),
            json_response['data']['reqSpecMutation']['reqSpec']['owner']['id']
        )
