from api.models import *
from rest_framework import serializers

class debtorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Debtor
        fields = '__all__'

class workSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = '__all__'

class productSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'