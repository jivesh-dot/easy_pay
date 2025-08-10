from rest_framework import serializers
from .models import PaymentIntent

class PaymentIntentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentIntent
        fields = ['amount','currency','description']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be a positive number.")
        return value

class PaymentIntentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentIntent
        fields = ['id','amount','currency','description','status','created_at','updated_at']


class PaymentIdentifierSerializer(serializers.Serializer):
    identifier = serializers.UUIDField()


class PaymentStatusUpdateSerializer(PaymentIdentifierSerializer):
    status = serializers.ChoiceField(
        choices=[
            PaymentIntent.Status.PAID,
            PaymentIntent.Status.CANCELLED
        ]
    )