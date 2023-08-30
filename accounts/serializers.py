from django.conf import settings
from rest_framework import serializers

from accounts.models import Account, Transaction


class AccountSerializer(serializers.Serializer):
    id = serializers.UUIDField(format='hex_verbose')
    user = serializers.RelatedField(source='settings.AUTH_USER_MODEL', read_only=True)
    name = serializers.CharField(max_length=200)
    # transaction_count_last_thirty_days = serializers.IntegerField(
    #     max_value=None, min_value=None)
    # balance_change_last_thirty_days = serializers.FloatField(
    #     max_value=None, min_value=None)

    class Meta:
        model = Account
        fields = '_all_'


class TransactionSerializer(serializers.Serializer):
    account = serializers.RelatedField(source='Account', read_only=True)
    # timestamp = serializers.DateTimeField(format=api_settings.DATETIME_FORMAT, input_formats=None, default_timezone=None)
    timestamp = serializers.DateTimeField()
    amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    description = serializers.CharField(max_length=100)
    transaction_category = serializers.CharField(max_length=20)

    class Meta:
        model = Transaction
        fields = '_all_'
