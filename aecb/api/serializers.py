from rest_framework import serializers
from aecb.api.models import Client, CreditCard, Employee, Account, Insurance, PreapprovalRequest, Promotion, Report


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = "__all__"


class InsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insurance
        fields = "__all__"


class CreditCardSerializerWithDepth(serializers.ModelSerializer):
    """
    This has depth enabled so it is easy to fetch credit cards
    with all the information related to the promotions or
    insurances associated to each card.
    """
    class Meta:
        model = CreditCard
        fields = "__all__"
        depth = 1


class CreditCardSerializer(serializers.ModelSerializer):
    """
    This serializer has depth disabled so it is easy to write
    new credit cards associated to promotions or insurances
    """
    class Meta:
        model = CreditCard
        fields = "__all__"


class PreapprovalRequestSerializerWithDepth(serializers.ModelSerializer):
    """
    This has depth enabled so it is easy to fetch preapproval
    request with all the information related to the client,
    credit card and employee associated to each card.
    """
    class Meta:
        model = PreapprovalRequest
        fields = "__all__"
        depth = 1


class PreapprovalRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreapprovalRequest
        fields = "__all__"


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = "__all__"


class ReportSerializerWithDepth(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = "__all__"
        depth = 2
