import graphene
from graphene import ObjectType, relay
from graphene_django.forms.mutation import DjangoModelFormMutation
from graphql_relay import from_global_id

from accounts.graphql.types import UserNode
from accounts.models import User
from customer.graphql.customer.types import CustomerNode
from .types import PrefSpecNode, ProformaSpecInput, ProformaNode
from ..forms.forms import ProformaModelForm, PrefSpecForm
from ...models import ReqSpec, PrefSpec, Xpref
from utils.graphql import utils as graphql_utils


class ProformaModelFormMutation(DjangoModelFormMutation):
    class Meta:
        form_class = ProformaModelForm

    @classmethod
    def get_form_kwargs(cls, root, info, **input):
        owner = info.context.user
        owner = User.objects.get(pk=4)
        input['owner'] = str(owner.pk)
        attrs = ['req_id']
        input = graphql_utils.from_globad_bulk(attrs, input)

        kwargs = {"data": input}
        if "id" not in input:
            last = Xpref.objects.order_by('number').last()
            input['number'] = last.number + 1
        else:
            input.pop("number")

        global_id = input.pop("id", None)
        if global_id:
            node_type, pk = from_global_id(global_id)
            instance = cls._meta.model._default_manager.get(pk=pk)
            kwargs["instance"] = instance
            input['number'] = instance.number
            input['req_id'] = instance.req_id.pk
        return kwargs


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


class DeleteProforma(relay.ClientIDMutation):

    class Input:
        proforma_id = graphene.ID()

    msg = graphene.String()
    prof = graphene.Field(ProformaNode)
    number = graphene.Int()

    @classmethod
    def mutate_and_get_payload(cls, root, info, proforma_id):
        pid = from_global_id(proforma_id)[1]
        proforma = Xpref.objects.get(pk=pid)
        proforma.delete()
        return cls(
            msg=f"پیش فاکتور شماره {proforma.number} با موفقیت حذف گردید.",
            number=proforma.number
        )


class ProformaModelMutation(ObjectType):
    proforma_mutation = ProformaModelFormMutation.Field()
    prefspec_mutation = PrefSpecModelFormMutation.Field()
    create_pref_specs_bulk = CreateProformaSpecBatch.Field()
    delete_proforma = DeleteProforma.Field()
