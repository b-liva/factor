import graphene
from graphene import ObjectType, relay
from graphene_django.forms.mutation import DjangoModelFormMutation
from graphql_relay import from_global_id

from .types import PrefSpecNode, ProformaSpecInput
from ..forms.forms import ProformaModelForm, PrefSpecForm
from ...models import ReqSpec, PrefSpec, Xpref


class ProformaModelFormMutation(DjangoModelFormMutation):
    class Meta:
        form_class = ProformaModelForm


class PrefSpecModelFormMutation(DjangoModelFormMutation):
    class Meta:
        form_class = PrefSpecForm


class CreateProformaSpecBatch(relay.ClientIDMutation):
    class Input:
        proforma_id = graphene.ID()
        specs_list = graphene.List(ProformaSpecInput)

    proforma_specs = graphene.List(PrefSpecNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, proforma_id, specs_list):
        print('proforma id: ', proforma_id)
        proforma_spec_list = []
        proforma = Xpref.objects.get(pk=from_global_id(proforma_id)[1])
        proforma.prefspec_set.all().delete()
        for spec in specs_list:
            print('these are specs: ', spec)
            spec.price = 0 if spec.price is None else spec.price
            order_spec = ReqSpec.objects.get(pk=from_global_id(spec.id)[1])
            proforma_spec = PrefSpec.objects.create(
                code=order_spec.code,
                owner=order_spec.owner,
                xpref_id=proforma,
                reqspec_eq=order_spec,
                qty=spec.qty,
                kw=order_spec.kw,
                rpm=order_spec.rpm_new.rpm,
                voltage=order_spec.voltage,
                ip=order_spec.ip,
                im=order_spec.im,
                ic=order_spec.ic,
                is_active=True,
                price=spec.price,
                summary=order_spec.summary
            )
            proforma_spec_list.append(proforma_spec)
        print('Done successfully....')
        return CreateProformaSpecBatch(proforma_specs=proforma_spec_list)


class ProformaModelMutation(ObjectType):
    proforma_mutation = ProformaModelFormMutation.Field()
    prefspec_mutation = PrefSpecModelFormMutation.Field()
    create_pref_specs_bulk = CreateProformaSpecBatch.Field()
