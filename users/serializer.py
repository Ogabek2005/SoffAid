from rest_framework import serializers
from django.utils import timezone
from users.utils import send_code
from . import models
import re
def validator(value):
    regex = r"^\+998\d{9}$"

    if not re.fullmatch(regex, value):
        raise serializers.ValidationError({"msg": "not a valid phone number"})

class SignUpSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        max_length=13,
        min_length=13,
        validators=[validator]
    )
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        phone = validated_data.get('phone_number')
        password = validated_data.get('password')
        user = models.User.objects.filter(phone_number=phone).first()

        if user:
            if user.auth_status:
                raise serializers.ValidationError({'msg': 'This phone number is already in use'})
        else:   
            user = models.User.objects.create_user(phone_number=phone, password=password)


        send_code(user.phone_number, user.get_code())
        
        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['tokens'] = instance.tokens()
        return data


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        validators=[validator], max_length=13, min_length=13
    )
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')
        user = models.User.objects.filter(phone_number=phone_number).first()

        if not user:
            raise serializers.ValidationError({"msg": "User does not exist!"})

        if not user.check_password(password):
            raise serializers.ValidationError({"msg": "Password does not match"})
        
        self.instance = user
        return attrs

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['tokens'] = instance.tokens()
        return data


class VerifySerializer(serializers.Serializer):
    code = serializers.CharField()

    def validate(self, attrs):
        user = self.context['request'].user
        code = attrs.get('code')
        now = timezone.now()

        if user.auth_status:
            raise serializers.ValidationError({'msg': ' Authorization status must be'})
        confirmation = user.confirmation
        if confirmation.code != code or now > confirmation.expire_time:
            raise serializers.ValidationError({'msg':'Code don\'t match'})
        
        user.auth_status = True

        user.save()
        return attrs