from rest_framework import serializers
from .models import Leaves

class LeavesSerializer(serializers.ModelSerializer):
    class Meta :
        model = Leaves
        fields =['from_date', 'till_date', 'reason']
        # fields = '__all__'

        def create(self, validated_data):
            leave_status = Leaves.leave_status
            user = Leaves(
                            from_date = validated_data['from_date'],
                            till_date = validated_data['till_date'],
                            reaason = validated_data['reason']
                            )
            
class AllLeavesSerializer(serializers.ModelSerializer):
    class Meta :
        model = Leaves
        fields = '__all__'

class UpdateLeaveSerializer(serializers.Serializer):
    leave_id = serializers.CharField()
    leave_status = serializers.IntegerField()