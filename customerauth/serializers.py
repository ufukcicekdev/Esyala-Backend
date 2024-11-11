from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import *
import re
from rest_framework.response import Response
from rest_framework import status
from .tcknrequest import TCKimlikNoSorgula
from django.contrib.auth import get_user_model, authenticate, update_session_auth_hash


User = get_user_model()

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
 
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['email'] = user.email
        token['username'] = user.username
        try:
            token['vendor_id'] = user.vendor.id
        except:
            token['vendor_id'] = 0
        return token
    


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Parolalar eşleşmiyor! Tekrar deneyin."})
        
        password1 = attrs['password']
        if len(password1) < 8:
            raise serializers.ValidationError({"password" : 'Şifreniz en az 8 karakter uzunluğunda olmalıdır.'})
        if not re.search(r'[A-Z]', password1):
            raise serializers.ValidationError({"password" : 'Şifreniz en az bir büyük harf içermelidir.'})
        if not re.search(r'[a-z]', password1):
            raise serializers.ValidationError({"password" : 'Şifreniz en az bir küçük harf içermelidir.'}  )
        if not re.search(r'[0-9]', password1):
            raise serializers.ValidationError({"password" : 'Şifreniz en az bir rakam içermelidir.'} )

        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "Bu e-posta adresi zaten kullanılıyor."})
        
        return attrs

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        
        user.set_password(validated_data['password'])
        user.save()

        return user 
    

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email:
            raise serializers.ValidationError({"email": "Email alanı boş olamaz."})
        if not password:
            raise serializers.ValidationError({"password": "Şifre alanı boş olamaz."})

        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError({"detail": "Geçersiz giriş bilgileri."})
        
        if not user.is_active:
            raise serializers.ValidationError({"detail": "Bu hesap aktif değil."})

        data['user'] = user
        return data




class NotificationSettingsSerializer(serializers.ModelSerializer):
    receive_email_notifications = serializers.BooleanField(required=True, error_messages={
        "required": "E-posta bildirim tercih alanı gereklidir.",
        "invalid": "E-posta bildirimi tercihi yalnızca doğru veya yanlış (True/False) olabilir."
    })
    receive_sms_notifications = serializers.BooleanField(required=True, error_messages={
        "required": "SMS bildirim tercih alanı gereklidir.",
        "invalid": "SMS bildirimi tercihi yalnızca doğru veya yanlış (True/False) olabilir."
    })

    class Meta:
        model = User 
        fields = ['receive_email_notifications', 'receive_sms_notifications']
    
    def validate(self, data):
        # Alanlar için özel doğrulama
        if not isinstance(data.get('receive_email_notifications'), bool):
            raise serializers.ValidationError({
                "receive_email_notifications": "E-posta bildirim tercihi geçerli bir Boolean değeri olmalıdır."
            })
        if not isinstance(data.get('receive_sms_notifications'), bool):
            raise serializers.ValidationError({
                "receive_sms_notifications": "SMS bildirim tercihi geçerli bir Boolean değeri olmalıdır."
            })
        return data
    
    def update(self, instance, validated_data):
        try:
            instance.receive_email_notifications = validated_data.get('receive_email_notifications', instance.receive_email_notifications)
            instance.receive_sms_notifications = validated_data.get('receive_sms_notifications', instance.receive_sms_notifications)
            instance.save()
        except Exception as e:
            raise serializers.ValidationError(f"Bildirim ayarları güncellenirken bir hata oluştu: {str(e)}")
        
        return instance


class ProfileUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        write_only=True,
        required=True,
        allow_blank=False,
        error_messages={"blank": "Kullanıcı adı boş bırakılamaz."}
    )
    first_name = serializers.CharField(
        write_only=True,
        required=True,
        allow_blank=False,
        error_messages={"blank": "Ad boş bırakılamaz."}
    )
    last_name = serializers.CharField(write_only=True, required=True, allow_blank=False,
        error_messages={"blank": "Ad boş bırakılamaz."})

    email = serializers.EmailField(
        write_only=True, 
        required=True, 
        error_messages={
            "invalid": "Lütfen geçerli bir e-posta adresi girin"
        }
    ) 
    birth_date = serializers.DateField(write_only=True, required=True)
    tckn = serializers.CharField(
        write_only=True,
        required=True,
        min_length=11,
        max_length=11,
        error_messages={
        "min_length": "TC Kimlik numarası 11 haneli olmalıdır.",
        "max_length": "TC Kimlik numarası 11 haneli olmalıdır."
    },
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'birth_date', 'tckn']
        
    def validate_tckn(self, value):
        if not value.isdigit():
            raise serializers.ValidationError('TC Kimlik No yalnızca sayısal karakterler içermelidir.')
        
        if len(value) != 11:
            raise serializers.ValidationError('TC Kimlik No 11 haneli olmalıdır.')
        
        if User.objects.filter(tckn=value).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError('Bu TC Kimlik No zaten başka bir kullanıcı tarafından kullanılıyor.')
        
        return value

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        
        tc_kimlik_no = validated_data.get('tckn')
        ad = instance.first_name
        soyad = instance.last_name
        dogum_yili = instance.birth_date.year
        
        sorgu = TCKimlikNoSorgula(tc_kimlik_no, ad, soyad, dogum_yili)
        sonuc = sorgu.sorgula()
        
        if sonuc:
            instance.verified = True  # Doğrulandıysa verified alanını güncelle
        else:
            raise serializers.ValidationError({"tckn": "TC Kimlik No doğrulanamadı."})
        
        instance.save()
        return instance
    


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password1 = serializers.CharField(
        required=True, 
        write_only=True, 
        validators=[validate_password]
    )
    new_password2 = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError({"new_password2": "Yeni şifreler eşleşmiyor."})
        
        password = data['new_password1']
        
        if len(password) < 8:
            raise serializers.ValidationError({"new_password1": "Şifreniz en az 8 karakter uzunluğunda olmalıdır."})
        if not re.search(r'[A-Z]', password):
            raise serializers.ValidationError({"new_password1": "Şifreniz en az bir büyük harf içermelidir."})
        if not re.search(r'[a-z]', password):
            raise serializers.ValidationError({"new_password1": "Şifreniz en az bir küçük harf içermelidir."})
        if not re.search(r'[0-9]', password):
            raise serializers.ValidationError({"new_password1": "Şifreniz en az bir rakam içermelidir."})
        
        return data

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Eski şifre doğru değil."})
        return value

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password1'])
        user.save()
        update_session_auth_hash(self.context['request'], user)
        return user
    



class EmailChangeSerializer(serializers.Serializer):
    new_email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)
    old_email = serializers.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        self.user = self.context['request'].user
        super().__init__(*args, **kwargs)
        if not self.initial_data.get('old_email'):
            self.initial_data['old_email'] = self.user.email

    def validate_password(self, value):
        if not authenticate(username=self.user.email, password=value):
            raise serializers.ValidationError("Mevcut şifreniz yanlış.")
        return value

    def validate_new_email(self, value):
        if User.objects.filter(email=value).exclude(pk=self.user.pk).exists():
            raise serializers.ValidationError("Bu e-posta adresi başka bir hesap tarafından kullanılıyor.")
        return value

    def validate(self, data):
        if data['new_email'] == data['old_email']:
            raise serializers.ValidationError({"new_email": "Yeni e-posta adresi eski e-posta adresinizle aynı olamaz."})
        return data