from rest_framework import serializers
from .models import Leaves

class LeavesSerializer(serializers.ModelSerializer):
    class Meta :
        model = Leaves
        fields =['employee','from_date', 'till_date', 'reason']
        # fields = '__all__'

        def create(self, validated_data):
            user = Leaves(employee = validated_data["employee"],
                            from_date = validated_data['from_date'],
                            till_date = validated_data['till_date'],
                            reaason = validated_data['reason']
                            )