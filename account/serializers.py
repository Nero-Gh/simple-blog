from rest_framework import serializers
from rest_framework.validators import ValidationError
from rest_framework.authtoken.models import Token
from .models import CustomUser



class SignUpSerializer(serializers.ModelSerializer):
    email=serializers.CharField(max_length=80)
    username=serializers.CharField(max_length=45)
    password=serializers.CharField(min_length=8,write_only=True)

    
    class Meta:
        model=CustomUser
        fields=['email','username','password']


    def validate(self, attrs):
        email_exits=CustomUser.objects.filter(email=attrs['email']).exists()

        if email_exits:
            raise ValidationError("Email already in use")
        return super().validate(attrs)
    
    
    def create(self, validated_data):
        password=validated_data.pop("password")

        user = super().create(validated_data) 
        print(user)
        user.set_password(password)
        user.save()
    
        Token.objects.create(user=user)
        print(user)
        return user
    


class CurrentUserPostSerializer(serializers.ModelSerializer):
    post=serializers.HyperlinkedRelatedField(many=True,view_name="post_detail",queryset=CustomUser.objects.all())

    class Meta:
        model=CustomUser
        fields=['id','username','email','post']

    


