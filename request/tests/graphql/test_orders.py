import json
from graphene_django.utils.testing import GraphQLTestCase

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
        mutation = '''
            mutation ReqMutation(
                $customer: ID!
                $owner: ID!
                $colleague: [ID]
            ){
              requestMutation(input:{
                customer: $customer
                owner:$owner
                pubDate: "1992-10-09T00:00:00Z", 
                clientMutationId:"klsjf"
                number:18665
                colleagues:$colleague
                dateFa: "1398-02-12"
                summary: "something about this request"
                isActive:true
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
        response = self.query(mutation,
                              variables={
                                  'customer': self.customer.pk,
                                  'owner': self.ex_user.pk,
                                  'colleague': self.user.pk
                              })
        json_response = json.loads(response.content)
        self.assertTrue('data' in json_response)

        self.assertEqual(json_response['data']['requestMutation']['requests']['number'], 18665)
        self.assertEqual(json_response['data']['requestMutation']['requests']['customer']['name'], 'zsamplecustomer')

    def test_request_mutation_no_customer_fail(self):
        """Test request mutation fails with no customer"""
        mutation = '''
                    mutation ReqMutation(
                        $customer: ID!
                        $owner: ID!
                        $colleague: [ID]
                    ){
                      requestMutation(input:{
                        owner:$owner
                        pubDate: "1992-10-09T00:00:00Z", 
                        clientMutationId:"klsjf"
                        number:18665
                        colleagues:$colleague
                        dateFa: "1398-02-12"
                        summary: "something about this request"
                        isActive:true
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
        response = self.query(mutation,
                              variables={
                                  'owner': self.ex_user.pk,
                                  'colleague': self.user.pk
                              })
        json_response = json.loads(response.content)
        self.assertFalse('data' in json_response)
        self.assertTrue('errors' in json_response)

    def test_request_mutation_no_number_fail(self):
        """Test request mutation fails with no number provided."""
        mutation = '''
                            mutation ReqMutation(
                                $customer: ID!
                                $owner: ID!
                                $colleague: [ID]
                            ){
                              requestMutation(input:{
                                owner:$owner
                                customer:$customer
                                pubDate: "1992-10-09T00:00:00Z", 
                                clientMutationId:"klsjf"
                                colleagues:$colleague
                                dateFa: "1398-02-12"
                                summary: "something about this request"
                                isActive:true
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
        response = self.query(mutation,
                              variables={
                                  'customer': self.customer.pk,
                                  'owner': self.ex_user.pk,
                                  'colleague': self.user.pk
                              })
        json_response = json.loads(response.content)
        self.assertFalse('data' in json_response)
        self.assertTrue('errors' in json_response)

    def test_request_mutation_number_exists_fail(self):
        """Test request mutation fails when number exists"""
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
                                pubDate: "1992-10-09T00:00:00Z", 
                                clientMutationId:"klsjf"
                                number:$number
                                colleagues:$colleague
                                dateFa: "1398-02-12"
                                summary: "something about this request"
                                isActive:true
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
        response = self.query(mutation,
                              variables={
                                  'owner': self.ex_user.pk,
                                  'colleague': self.user.pk,
                                  'number': self.req.number
                              })
        json_response = json.loads(response.content)
        # todo: more assertion to test errors.
        self.assertFalse('data' in json_response)
        self.assertTrue('errors' in json_response)

    def test_request_mutation_future_date_fail(self):
        pass

    def test_reqspec_mutation_success(self):
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
        response = self.query(mutation, variables={
            'reqId': req.pk,
            'owner': self.ex_user.pk,
            'type': self.project_type.pk,
            'rpm_new': self.rpm_new.pk
        })
        json_response = json.loads(response.content)
        reqspec = req.reqspec_set.last()
        self.assertEqual(reqspec.kw, json_response['data']['reqSpecMutation']['reqSpec']['kw'])
        self.assertEqual(reqspec.rpm, json_response['data']['reqSpecMutation']['reqSpec']['rpm'])
        self.assertEqual(reqspec.voltage, json_response['data']['reqSpecMutation']['reqSpec']['voltage'])
        self.assertEqual(reqspec.qty, json_response['data']['reqSpecMutation']['reqSpec']['qty'])

    def test_reqspec_mutation_no_kw_fail(self):
        """Test reqspec mutation fails with no kw provided."""
        pass

    def test_reqspec_mutation_no_qty_fail(self):
        """Test reqspec mutation fails with no qty provided."""
        pass

    def test_reqspec_mutation_no_rpm_fail(self):
        """Test reqspec mutation fails with no rpm provided."""
        pass

    def test_reqspec_mutation_no_voltage_fail(self):
        """Test reqspec mutation fails with no voltage provided."""
        pass
