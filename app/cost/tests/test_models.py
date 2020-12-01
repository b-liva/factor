import re
import jdatetime
from django.contrib.auth.models import Group, Permission
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from accounts.tests.test_public_funcs import CustomAPITestCase
from cost import models
from cost.models import ProjectCost

CREATE_COST_URL = reverse('cost:create')


def create_cost(client):
    custom_api = CustomAPITestCase()
    custom_api.sale_expert_group = Group.objects.create(name='sale_expert')
    exp_user = custom_api.sample_user(username='exp')
    exp_user.groups.add(custom_api.sale_expert_group)
    custom_api.sale_expert_group.permissions.add(
        Permission.objects.get(codename='add_projectcost', content_type__app_label='cost'),
    )
    client.force_authenticate(user=exp_user)

    cc = CreateCost()  # create cost
    payload = cc.create_total_cost()
    payload['owner'] = exp_user.pk
    return payload


class CreateCost:

    def __init__(self, **kwargs):
        self.ch_number = "9837"
        self.motor_type = "ls"
        self.standard_parts = 9832749892837
        self.cost_production = 912387498
        self.general_cost = 923874
        self.cost_practical = 298374982374

        self.wage_payload = {
            'qty': 1,
            'price': 2500,
            'unit': ('hr', 'hr')
        }
        self.steel_rebar_payload = {
            'qty': 1,
            'price': 2500,
            'unit': ('kg', 'kg')
        }

        self.overhead_payload = self.wage_payload
        self.cast_iron_payload = self.silicon_payload = self.alu_payload = self.cu_payload = self.steel_payload \
            = self.steel_rebar_payload
        self.bearing_payload = {
            'qty': 1,
            'price': 2500,
            'unit': ('count', 'count')
        }
        self.test_payload = {
            'qty': 1,
            'price': 2500,
            'unit': ('item', 'item')
        }
        self.certificate_payload = {
            'qty': 1,
            'price': 2500,
            'unit': ('item', 'item')
        }

        self.models_list = [
            models.WageCost,
            models.SteelRebar,
            models.OverheadCost,
            models.Steel,
            models.CuStator,
            models.AluIngot,
            models.SiliconSheet,
            models.CastIron,
            models.Bearing,
            models.Test,
            models.Certificate,
        ]

    def modify_model_names(self):
        """todo: This should generate function based on model names"""
        # func_template = f"""def create_{x}(self, **kwargs): return models.{y}.objects.create(**kwargs)"""
        modified_model_names = dict()
        for name in self.models_list:
            x = re.findall('[A-Z][^A-Z]*', name.__name__)
            x = [i.lower() for i in x]
            modified_model_names['_'.join(x)] = name

        return modified_model_names

    def create_wage(self, **kwargs):
        return models.WageCost.objects.create(**kwargs)

    def create_steel_rebar(self, **kwargs):
        return models.SteelRebar.objects.create(**kwargs)

    def create_overhead(self, **kwargs):
        return models.OverheadCost.objects.create(**kwargs)

    def create_steel(self, **kwargs):
        return models.Steel.objects.create(**kwargs)

    def create_cu(self, **kwargs):
        return models.CuStator.objects.create(**kwargs)

    def create_alu(self, **kwargs):
        return models.AluIngot.objects.create(**kwargs)

    def create_silicon(self, **kwargs):
        return models.SiliconSheet.objects.create(**kwargs)

    def create_cast_iron(self, **kwargs):
        return models.CastIron.objects.create(**kwargs)

    def create_bearing(self, **kwargs):
        return models.Bearing.objects.create(**kwargs)

    def create_test(self, **kwargs):
        return models.Test.objects.create(**kwargs)

    def create_certificate(self, **kwargs):
        return models.Certificate.objects.create(**kwargs)

    def create_total_cost(self, **kwargs):
        owner = kwargs.get('owner', None)
        wage = self.create_wage(**self.wage_payload)
        steel_rebar = self.create_steel_rebar(**self.steel_rebar_payload)
        overhead = self.create_overhead(**self.overhead_payload)
        steel = self.create_steel(**self.steel_payload)
        cu = self.create_cu(**self.cu_payload)
        alu = self.create_alu(**self.alu_payload)
        silicon = self.create_silicon(**self.silicon_payload)
        cast_iron = self.create_cast_iron(**self.cast_iron_payload)
        bearing = self.create_bearing(**self.bearing_payload)
        test = self.create_test(**self.test_payload)
        certificate = self.create_certificate(**self.certificate_payload)
        ch_number = self.ch_number
        standard_parts = self.standard_parts
        motor_type = self.motor_type
        cost_production = self.cost_production
        general_cost = self.general_cost
        cost_practical = self.cost_practical
        date_fa = jdatetime.date.today()

        payload = {
            'owner': owner.pk if owner else None,
            'wage': wage.pk,
            'steel_rebar': steel_rebar.pk,
            'overhead': overhead.pk,
            'steel': steel.pk,
            'cu': cu.pk,
            'alu': alu.pk,
            'silicon': silicon.pk,
            'cast_iron': cast_iron.pk,
            'ch_number': ch_number,
            'motor_type': motor_type,
            'date_fa': date_fa,
            'bearing': bearing.pk,
            'test': test.pk,
            'certificate': certificate.pk,
            'standard_parts': standard_parts,
            'cost_production': cost_production,
            'general_cost': general_cost,
            'cost_practical': cost_practical,
        }
        return payload


class PublicCostAPITest(CustomAPITestCase):
    """Test the user API (public)"""

    def setUp(self):
        super().setUp()
        self.client_anon = APIClient()
        self.client_exp = APIClient()
        self.client_exp.force_authenticate(user=self.ex_user)
        cc = CreateCost()
        self.payload = cc.create_total_cost()

        self.payload['owner'] = self.ex_user.pk
        res = self.client_exp.post(CREATE_COST_URL, self.payload)
        self.sample_cost = ProjectCost.objects.get(pk=res.data['id'])

    def test_list_cost_unauthenticated(self):
        """Test that authentication is required for listing cost"""
        res = self.client_anon.get(CREATE_COST_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_cost_unauthenticated(self):
        """Test that authentication is required for creating cost"""
        res = self.client_anon.post(CREATE_COST_URL, self.payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_cost_fail_unauthenticated(self):
        """Test that anonymous user can't update cost"""
        self.payload['practical_cost'] = 1232
        url = reverse('cost:manage', kwargs={'pk': self.sample_cost.pk})
        res = self.client_anon.put(url, self.payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_cost_fail_unauthenticated(self):
        """Test that anonymous user can't update cost"""
        url = reverse('cost:manage', kwargs={'pk': self.sample_cost.pk})
        res = self.client_anon.delete(url)
        exists = ProjectCost.objects.filter(pk=self.sample_cost.pk).exists()
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(exists)


class PrivateCostAPITest(CustomAPITestCase):
    def setUp(self):
        super().setUp()
        self.client_anon = APIClient()
        self.client.force_authenticate(user=self.user)
        self.client_exp = APIClient()
        self.client_exp.force_authenticate(user=self.ex_user)
        self.client_superuser = APIClient()
        self.client_superuser.force_authenticate(user=self.superuser)

        cc = CreateCost()  # create cost
        self.payload = cc.create_total_cost()
        self.payload['owner'] = self.ex_user.pk

        res = self.client_exp.post(CREATE_COST_URL, self.payload)
        self.sample_cost = ProjectCost.objects.get(pk=res.data['id'])

    def test_create_cost_fails_unauthorized(self):
        """Test that authenticated user with no permission can't create cost(get)"""
        res = self.client.get(CREATE_COST_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_cost_post_fails_unauthorized(self):
        """Test that authenticated user with no permission can't create cost(post)"""
        self.payload['owner'] = self.user.pk
        res = self.client.post(CREATE_COST_URL, self.payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_cost_post_success(self):
        """Test that authorized user can create cost"""
        self.payload['owner'] = self.ex_user.pk
        res = self.client_exp.post(CREATE_COST_URL, self.payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['wage'], self.payload['wage'])
        self.assertEqual(res.data['owner'], self.payload['owner'])

    def test_retrieve_cost_fails_unauthorized(self):
        """Test that user with no permission can't retrieve cost"""

        url = reverse('cost:manage', kwargs={'pk': self.sample_cost.pk})
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_update_cost_fails_unauthorized(self):
        """Test that user with no permission can't update cost"""
        self.payload['cost_practical'] = 1233

        url = reverse('cost:manage', kwargs={'pk': self.sample_cost.pk})
        res = self.client.put(url, self.payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_cost_fails_unauthorized(self):
        """Test that user with no permission can't update cost"""
        url = reverse('cost:manage', kwargs={'pk': self.sample_cost.pk})
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_cost_success(self):
        """Test that user with update permission can update cost"""
        url = reverse('cost:manage', kwargs={'pk': self.sample_cost.pk})
        self.payload['cost_practical'] = 123
        res = self.client_exp.put(url, self.payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['cost_practical'], self.payload['cost_practical'])

    def test_delete_cost_success(self):
        """Test that user with delete permission can delete cost"""
        cost_pk = self.sample_cost.pk
        url = reverse('cost:manage', kwargs={'pk': cost_pk})

        res = self.client_exp.delete(url)

        exists = ProjectCost.objects.filter(pk=cost_pk).exists()
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(exists)
