import graphene
from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.forms.mutation import DjangoModelFormMutation, DjangoFormMutation

from graphql_relay import from_global_id

from .types import CustomerNode
from customer.forms import CustomerForm

from customer.models import Customer
from django import forms


class MyForm(forms.Form):
    test_field = forms.CharField()


class MyMutation(DjangoFormMutation):

    class Meta:
        form_class = MyForm

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        return cls(test_field=input.get('test_field'))


class MyModelForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"


class MyModelFormMutation(DjangoModelFormMutation):

    class Meta:
        form_class = MyModelForm

    # @classmethod
    # def mutate_and_get_payload(cls, root, info, **input):
    #     print('mutating model form')
    #     print(input)
    #     form = cls.get_form(root, info, **input)
    #     print(form)
    #     return super().mutate_and_get_payload(root, info, **input)
    @classmethod
    def perform_mutate(cls, form, info):
        print("This only runs when the form is valid")
        return super().perform_mutate(form, info)


class CustomerModelMutations(ObjectType):
    customer_mutation = MyMutation.Field()
    customer_model_mutation = MyModelFormMutation.Field()
