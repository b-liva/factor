import graphene
from django.core.exceptions import ValidationError
from graphene import relay, ObjectType, InputObjectType
from graphene_django import DjangoObjectType
from graphene_django.forms.mutation import DjangoModelFormMutation, DjangoFormMutation
from graphene_django.rest_framework.mutation import SerializerMutation
from graphql_relay import from_global_id

from .types import CustomerNode
from customer.forms import CustomerForm
from .types import CustomerNode
from customer.drf.serializers import CustomerSerializer

from customer.models import Customer
from django import forms, http
from utils.graphql import utils as graphql_utils


class MyForm(forms.Form):
    test_field = forms.CharField()


class MyMutation(DjangoFormMutation):

    class Meta:
        form_class = MyForm

    # probably this is the choice with django forms
    # @classmethod
    # def perform_mutate(cls, form, info):
    #     pass

    # And this is the choice with relay.
    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        return cls(test_field=input.get('test_field'))


class CustomerModelform(forms.ModelForm):
    # customer_id = forms.CharField()

    # def __init__(self, data=None, *args, **kwargs):
    #     # data = kwargs.get('data')
    #     # instance = kwargs.get('instance', None)
    #     # if instance:
    #     #     print(instance.pk)
    #     attrs = ['owner', 'type']
    #     if data is not None:
    #         for attr in attrs:
    #             if attr in data:
    #                 print('attr: ', attr)
    #                 data[attr] = from_global_id(data[attr])[1]
    #         # if 'customer_id' in data:
    #         #     # data['pk'] = from_global_id(data['customer_id'])[1]
    #         #     print(data)
    #     super(CustomerModelform, self).__init__(data, args, kwargs)

    class Meta:
        model = Customer
        fields = "__all__"


    # def clean(self):
    #     print('clean', self.cleaned_data)
    #
    #     print(self.changed_data)
    #     return super(MyModelForm, self).clean()

    # def clean_date2(self):
    #     print('cleaning owner')

    # def is_valid(self):
    #     print('form validation')
    #     return super().is_valid()


# class CustomerType(DjangoObjectType):
#     class Meta:
#         model = Customer

class CreateCustomer(DjangoModelFormMutation):
    customer = relay.node.Field(CustomerNode)

    class Meta:
        form_class = CustomerModelform

    # @classmethod
    # def mutate_and_get_payload(cls, root, info, **input):
    #     print('mutating model form')
    #     print(input)
    #     form = cls.get_form(root, info, **input)
    #     print(form)
    #     return super().mutate_and_get_payload(root, info, **input)

    @classmethod
    def perform_mutate(cls, form, info, **kwargs):
        print("This only runs when the form is valid")
        return super().perform_mutate(form, info)

    @classmethod
    def get_form_kwargs(cls, root, info, **input):
        owner = info.context.user
        input['owner'] = str(owner.pk)
        attrs = ['type']
        input = graphql_utils.from_globad_bulk(attrs, input)
        kwargs = {"data": input}

        global_id = input.pop("id", None)
        if global_id:
            node_type, pk = from_global_id(global_id)
            instance = cls._meta.model._default_manager.get(pk=pk)
            kwargs["instance"] = instance

        return kwargs


class CustomerCreateInput(InputObjectType):
    name = graphene.String(required=False)
    owner = graphene.String()
    type = graphene.String()
    date2 = graphene.String()
    pub_date = graphene.DateTime()


class UpdateCustomer(relay.ClientIDMutation):

    class Input:
        customer = graphene.Argument(CustomerCreateInput)
        id = graphene.String(required=True)

    def __init__(self, *args, **kwargs):
        print('the update class', args, kwargs)

        super(UpdateCustomer, self).__init__(args, kwargs)

    # class Meta:
    #     form_class = CustomerModelform

    errors = graphene.List(graphene.String)
    updated_customer = graphene.Field(CustomerNode)

    # def perform_mutate(cls, form, info):
    #     print(cls)
    #     print(form)
    #     super(UpdateCustomer, cls).perform_mutate(form, info)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        try:
            customer_instance = get_object(Customer, input['id'])
            input['customer']['id'] = input['id']
            if customer_instance:
                form = CustomerModelform(input['customer'] or None, instance=customer_instance)
                updated_customer = form.save(commit=False)
                updated_customer.save()
                customer_data = input.get('customer')
                # updated_customer = update_create_instance(customer_instance, customer_data)
                return cls(updated_customer=updated_customer)
        except ValidationError as e:
            # return an error if something wrong happens
            return cls(updated_book=None, errors=get_errors(e))


def get_object(object_name, relayId, otherwise=None):
    try:
        return object_name.objects.get(pk=from_global_id(relayId)[1])
    except:
        return otherwise


def update_create_instance(instance, args, exception=['id']):
    if instance:
        [setattr(instance, key, value) for key, value in args.items() if key not in exception]

    # caution if you literally cloned this project, then be sure to have
    # elasticsearch running as every saved instance must go through
    # elasticsearch according to the way this project is configured.
    instance.save()

    return instance


def get_errors(e):
    # transform django errors to redux errors
    # django: {"key1": [value1], {"key2": [value2]}}
    # redux: ["key1", "value1", "key2", "value2"]
    fields = e.message_dict.keys()
    messages = ['; '.join(m) for m in e.message_dict.values()]
    errors = [i for pair in zip(fields, messages) for i in pair]
    return errors


class MyCustomerMutation(SerializerMutation):
    class Meta:
        serializer_class = CustomerSerializer
        lookup_field = 'id'

    updated_customer = graphene.Field(CustomerNode)

    @classmethod
    def get_serializer_kwargs(cls, root, info, **input):
        if 'id' in input:
            instance = Customer.objects.filter(
                id=input['id']
            ).first()
            if instance:
                return {'instance': instance, 'data': input, 'partial': True}
            else:
                raise http.Http404
        return {'data': input, 'partial': True}


class CustomerModelMutations(ObjectType):
    customer_mutation = MyMutation.Field()
    create_customer = CreateCustomer.Field()
    update_customer_mut = UpdateCustomer.Field()
    update_customer_ser = MyCustomerMutation.Field()
