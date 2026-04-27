from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "telegram_chat_id", "telegram_username")
        read_only_fields = ("id",)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
        )
        if validated_data.get("telegram_chat_id"):
            user.telegram_chat_id = validated_data["telegram_chat_id"]
        if validated_data.get("telegram_username"):
            user.telegram_username = validated_data["telegram_username"]
        user.save()
        return user
