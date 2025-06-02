from rest_framework import serializers
from .models import SpamMessage, SpamURL, SpamPhoneNumber

class SpamMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpamMessage
        fields = '__all__'

class SpamURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpamURL
        fields = '__all__'

class SpamPhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpamPhoneNumber
        fields = '__all__'
