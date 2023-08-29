from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta :
        model = CustomUser
        fields = ['email','password','first_name', 'last_name', 'contact_no', 'address','manager','role','created_at','modified_at']
        extra_kwargs = {
               'password' : {'write_only': True}
                        }
    
    def create(self, validated_data):
        role = validated_data.get('role')
        if role== 'manager':
            is_manager_field = True
        else:
            is_manager_field = False

        user = CustomUser(username = validated_data['email'],
                           email = validated_data['email'],
                           first_name = validated_data['first_name'],
                           last_name = validated_data['last_name'],
                           contact_no = validated_data['contact_no'],
                           address = validated_data['address'],
                           manager = validated_data['manager'],
                           role = role,
                           is_manager = is_manager_field
                           )
        user.set_password(validated_data['password'])
        user.save()
        return user



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
