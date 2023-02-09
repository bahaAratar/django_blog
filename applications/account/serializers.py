from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from applications.account.send_email import send_activation_code



User = get_user_model() # CustomUSer

class RegisterSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(
        required=True,
        min_length=6,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('email', 'password', 'password2')

    def validate_email(self, email):
        print('hello')
        return email

    def validate(self, attrs):
        p1 = attrs.get('password')
        p2 = attrs.pop('password2')

        if p1 != p2:
            raise serializers.ValidationError('password did not match!!!')

        return attrs


    def create(self, validate_data):
        user = User.objects.create_user(**validate_data) 
        send_activation_code(user.email, user.activation_code)
        return user
        
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            return email

        raise serializers.ValidationError('пользователь не найден')

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(username=email, password=password) # None
        if not user:
            raise serializers.ValidationError('не верный пароль')

        attrs['user'] = user
        return attrs