from rest_framework import serializers

from users.models import User


class UserChangePassword(serializers.ModelSerializer):

    repeat_password = serializers.CharField(min_length=6, max_length=25, required=True, write_only=True)
    password = serializers.CharField(min_length=6, max_length=25, required=True, write_only=True)

    class Meta:
        model = User
        fields = ['password', 'repeat_password']

    def update(self, instance: User, validated_data):
        new_password = validated_data.get("new_password")
        instance.set_password(new_password)
        instance.save()
        return instance
