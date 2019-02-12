from rest_framework.serializers import ModelSerializer, SerializerMethodField
from fund.models import Fund


class FundCreateSerializer(ModelSerializer):
    class Meta:
        model = Fund
        exclude = [
            'owner',
        ]


class FundListSerializer(ModelSerializer):
    owner = SerializerMethodField()

    class Meta:
        model = Fund
        fields = [
            'id',
            'owner',
            'title',
        ]

    # this is doable for any of that above fields
    def get_owner(self, obj):
        return str(obj.owner.username) + ' --> This is done via, SerializerMethodField'


class FundDetailsSerializer(ModelSerializer):
    title = SerializerMethodField()

    class Meta:
        model = Fund
        # fields = '__all__'
        exclude = [
            'owner'
        ]

    def get_title(self, obj):
        return 'OK: this is new title from seriaizer: ' + str(obj.title)
