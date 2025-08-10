from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password


import users.models as user_models

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    business_name = serializers.CharField(write_only=True, required=True)
    email = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = user_models.User
        fields = ('email', 'password', 'business_name')

    def create(self, validated_data):
        business_name = validated_data.pop('business_name')
        validated_data['username'] = validated_data['email']
        user =user_models.User.objects.create_user(**validated_data)
        user_models.Merchant.objects.create(user=user, business_name=business_name)
        return user
