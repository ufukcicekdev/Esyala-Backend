from django.shortcuts import  get_object_or_404
from django.contrib.auth import authenticate, login
from .serializers import *
from rest_framework import status
from rest_framework.decorators import  APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView,TokenBlacklistView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from customerauth.send_confirmation import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from customerauth.models import *


class VerifyEmailView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            signer = TimestampSigner()
            user_pk = signer.unsign(token, max_age=86400)  # 24 saat geçerli
            user = User.objects.get(pk=user_pk)
            
            if not user.email_verified:
                user.email_verified = True
                user.save()
                return Response({ "status":True, "message": "E-posta adresiniz doğrulandı!"}, status=status.HTTP_200_OK)
            else:
                return Response({"status":True,"message": "E-posta zaten doğrulanmış."}, status=status.HTTP_400_BAD_REQUEST)
        except (User.DoesNotExist, BadSignature, SignatureExpired):
            return Response({"status":False,"messages": "Doğrulama bağlantısı geçersiz veya süresi dolmuş."}, status=status.HTTP_400_BAD_REQUEST)



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
  serializer_class = RegisterSerializer
  def post(self,request,format=None):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token = get_tokens_for_user(user)
        send_confirmation_email(user, request)
        return Response({ "status":True, "message": "Kayıt başarılı! Lütfen e-postanızı doğrulayın.", 
                         "token":token}, status=status.HTTP_201_CREATED)
    return Response({ "status":False, "messages":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class UserLoginView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            # Hata mesajlarını düzenleyerek döndür
            messages_list = []
            for key, value in serializer.errors.items():
                messages_list.extend(value)  # Her bir alanın hatalarını ekle
            
            return Response({
                "status": False,
                "message": messages_list  # Tüm hata mesajları bir liste olarak döner
            }, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')

        user = authenticate(username=email, password=password)

        if user is not None:
            if not user.email_verified:
                send_confirmation_email(user, request)
                return Response({
                    "status": True,
                    "message": "Lütfen e-postanızı doğrulayın."
                }, status=status.HTTP_201_CREATED)

            login(request, user)
            token = get_tokens_for_user(user)

            user_data = {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }

            return Response({
                "status": True,
                "token": token,
                "user": user_data,
                "message": "Giriş Başarılı"
            }, status=status.HTTP_200_OK)

        return Response({
            "status": False,
            "message": ["Email veya şifre yanlış."]
        }, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(TokenBlacklistView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = super().post(request)  
        return Response({"message": "Çıkış işlemi başarılı."}, status=status.HTTP_205_RESET_CONTENT)


class ProfileUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]  #TODO: düzetilecek
    serializer_class = ProfileUpdateSerializer
    
    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = ProfileUpdateSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Profiliniz başarıyla güncellendi."}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class NotificationSettingsAPI(APIView):
    permission_classes = [IsAuthenticated]    #TODO: düzetilecek
    serializer_class = NotificationSettingsSerializer
    def get(self, request):
        print("request.user",request.user)
        user_profile = get_object_or_404(User, id=request.user.id) 
        serializer = NotificationSettingsSerializer(user_profile)
        return Response(serializer.data)

    def put(self, request):
        user_profile = get_object_or_404(User, id=request.user.id) #request.user
        serializer = NotificationSettingsSerializer(user_profile, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Bildirimler Güncellendi"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


class PasswordChangeView(APIView):
    permission_classes = [AllowAny] #TODO: düzetilecek
    serializer_class = PasswordChangeSerializer

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Şifre başarıyla değiştirildi."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    




### MyStyle 


class ChangeEmailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = EmailChangeSerializer(data=request.data, context={'request': request})
        messages_list = []

        if serializer.is_valid():
            new_email = serializer.validated_data['new_email']
            old_email = serializer.validated_data['old_email']
            user = request.user

            user.email = new_email
            user.email_verified = True
            user.save()

            send_email_change_notification(new_email, user, old_email)

            messages_list.append({'message': 'E-posta adresiniz başarıyla güncellendi.', 'tags': 'success'})
            return Response({
                "status": True,
                "messages": messages_list
            }, status=status.HTTP_200_OK)
        
        else:
            # Hataları JSON olarak döndür
            errors = serializer.errors
            for field, error_list in errors.items():
                for error in error_list:
                    messages_list.append({'message': f"{field.capitalize()}: {error}", 'tags': 'warning'})

            return Response({
                "status": False,
                "messages": messages_list
            }, status=status.HTTP_400_BAD_REQUEST)