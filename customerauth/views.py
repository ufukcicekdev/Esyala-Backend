from django.shortcuts import  get_object_or_404
from django.contrib.auth import authenticate, login

from customerauth.AddressProcess.addressSerializers import AddressListSerializer, AddressSerializer
from esyala import settings
from products.serializers import CartSerializer
from .serializers import *
from rest_framework import status
from rest_framework.decorators import  APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView,TokenBlacklistView,TokenRefreshView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from customerauth.send_confirmation import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from customerauth.models import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.exceptions import AuthenticationFailed


class VerifyEmailView(APIView):
    def get(self, request, uidb64, token):
        print("uidb64",uidb64)
        print("token",token)

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            signer = TimestampSigner()
            
            user_pk = signer.unsign(token, max_age=86400)  # 24 saat geçerli
            user = User.objects.get(pk=user_pk)

            if not user.email_verified:
                user.email_verified = True
                user.save()
                return Response(
                    {"status": True, "message": "E-posta adresiniz başarıyla doğrulandı!"},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"status": True, "message": "E-posta zaten doğrulanmış."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except SignatureExpired:
            return Response(
                {"status": False, "message": "Doğrulama bağlantısının süresi dolmuş. Lütfen yeniden e-posta doğrulama isteğinde bulunun."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except BadSignature:
            return Response(
                {"status": False, "message": "Doğrulama bağlantısı geçersiz. Lütfen doğru bağlantıyı kullandığınızdan emin olun."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except User.DoesNotExist:
            return Response(
                {"status": False, "message": "Kullanıcı bulunamadı. Lütfen doğru bağlantıyı kullandığınızdan emin olun."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"status": False, "message": "Bir hata oluştu. Lütfen tekrar deneyin."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TokenVerifyView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            
            if not user.is_authenticated:
                raise AuthenticationFailed( 'User is not authenticated')

            vendor_id = None
            if hasattr(user, 'vendor') and user.vendor:
                vendor_id = user.vendor.id

            return Response({
                "status": True,
                "user": {
                    "username": user.username,
                    "email": user.email,
                    "vendor_id": vendor_id
                }
            })

        except AuthenticationFailed as e:
            return Response({
                "status": False,
                "message": str(e)
            }, status=status.HTTP_401_UNAUTHORIZED)  

        except Exception as e:
            return Response({
                "status": False,
                "message": f"An unexpected error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 




class CustomTokenRefreshView(TokenRefreshView):
    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return Response(
                { "status":False, "message": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        try:
            refresh = RefreshToken(refresh_token)
            access_token = refresh.access_token
            response = Response({
                "status":True,
                'access': str(access_token),
            })
            return response
        except Exception as e:
            return Response(
                { "status":False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )



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
    
    messages_list = []
    for key, value in serializer.errors.items():
        messages_list.extend(value) 
    return Response({ "status":False, "message": ",".join(messages_list) }, status=status.HTTP_400_BAD_REQUEST)



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
                "message": ",".join(messages_list)  # Tüm hata mesajları bir liste olarak döner
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
            token = get_tokens_for_user(user)  # Token'ları al

            # Çerezleri ayarlıyoruz
            response = Response({
                "status": True,
                "token": token,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                },
                "message": "Giriş Başarılı"
            }, status=status.HTTP_200_OK)

            # Çerezleri ayarla
            response.set_cookie(
                'access_token', 
                token['access'], 
                max_age=3600,  # 1 saat
                secure=True,  # Üretim ortamında secure=True olacak
                httponly=True,  # HttpOnly flag
                samesite='Strict',  # veya 'Lax'
                path='/'
            )

            response.set_cookie(
                'refresh_token', 
                token['refresh'], 
                max_age=7 * 24 * 60 * 60,  # 7 gün
                secure=True,  # Üretim ortamında secure=True olacak
                httponly=True,  # HttpOnly flag
                samesite='Strict',  # veya 'Lax'
                path='/'
            )

            return response

        return Response({
            "status": False,
            "message": "Email veya şifre yanlış."
        }, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh", None)
        if not refresh_token:
            return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist() 
            return Response({"status":True, "message": "Çıkış işlemi başarılı."}, status=status.HTTP_200_OK)
        
        except TokenError:  # InvalidToken yerine daha spesifik hata
            return Response({"status":False, "message": "Geçersiz token."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status":False, "message": "Bilinmeyen bir hata oluştu.", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request, *args, **kwargs):
        try:
            profile = get_object_or_404(User, id=request.user.id)  # Burada request.user.id kullanılmalı
        except User.DoesNotExist:
            return Response({"status": False, "message": "Profile not found"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProfileViewSerializer(profile)
        return Response({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)


class ProfileUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]  
    serializer_class = ProfileUpdateSerializer
    
    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = ProfileUpdateSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"status":True, "message": "Profiliniz başarıyla güncellendi."}, status=status.HTTP_200_OK)
        else:
            if not serializer.is_valid():
                messages_list = []
                for key, value in serializer.errors.items():
                    messages_list.extend(value) 
            return Response({ "status":False, "message":messages_list }, status=status.HTTP_400_BAD_REQUEST)
        

class NotificationSettingsAPI(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSettingsSerializer

    def get(self, request, *args, **kwargs):
        try:    
            user_profile = get_object_or_404(User, id=request.user.id)
            serializer = NotificationSettingsSerializer(user_profile)
            return Response({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        except:
            return Response({"status": False, "message": "Bir sorun oluştu"}, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        user_profile = get_object_or_404(User, id=request.user.id)
        serializer = NotificationSettingsSerializer(user_profile, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"status": True, "message": "Bildirimler Güncellendi"}, status=status.HTTP_200_OK)
        else:
            if not serializer.is_valid():
                messages_list = []
                for key, value in serializer.errors.items():
                    messages_list.extend(value) 
            return Response({ "status":False, "message":messages_list }, status=status.HTTP_400_BAD_REQUEST)
        


class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated] 
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
        




def generate_otp():
    return ''.join(random.choices('0123456789', k=6))

class PasswordResetRequestAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Gelen isteği serializer ile doğrulama
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)  # Kullanıcıyı bulma
                otp = generate_otp()  # OTP üretme
                PasswordReset.objects.create(user=user, otp=otp)  # OTP'yi veritabanına kaydetme
                
                # E-posta içeriğini oluşturma
                context = {
                    'username': user.username,
                    'otp': otp,
                }
                email_content = render_to_string('email_templates/reset_password_email.html', context)
                
   
                send_change_password_email([user.email], "Hesap Doğrulama", email_content)


                return Response({"message": "Doğrulama kodunuz e-posta adresinize gönderildi."}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "Bu e-posta adresi ile kayıtlı kullanıcı bulunamadı."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetVerifyAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Gelen isteği doğrulama
        serializer = PasswordResetVerifySerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            
            try:
                # OTP kontrolü
                password_reset = PasswordReset.objects.get(user__email=email, otp=otp)
                return Response({"message": "OTP doğrulandı. Şifrenizi değiştirebilirsiniz."}, status=status.HTTP_200_OK)
            except PasswordReset.DoesNotExist:
                return Response({"error": "Geçersiz OTP."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class PasswordResetChangePasswordAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Yeni şifreyi alalım
        new_password = request.data.get("new_password")
        otp = request.data.get("otp")
        email = request.data.get("email")
        
        try:
            # OTP ve kullanıcının şifresini kontrol et
            password_reset = PasswordReset.objects.get(user__email=email, otp=otp)
            user = password_reset.user
            
            # Yeni şifreyi kullanıcıya atama
            user.set_password(new_password)
            user.save()
            
            # OTP'yi geçersiz kılma
            password_reset.delete()

            return Response({"message": "Şifreniz başarıyla güncellendi."}, status=status.HTTP_200_OK)
        except PasswordReset.DoesNotExist:
            return Response({"error": "Geçersiz OTP."}, status=status.HTTP_400_BAD_REQUEST)
        


class CheckoutView(APIView):

    def get(self, request):
        # cart_id ile sepeti al
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)

        # Kullanıcının adreslerini al
        addresses = Address.objects.filter(user=request.user)

        # Sepet verisini serialize et
        cart_serializer = CartSerializer(cart).data
        
        # Adresleri serialize et
        address_serializer = AddressListSerializer(addresses, many=True)

        # Sepet ve adresleri birleştirip döndür
        return Response({
            'cart': cart_serializer,
            'addresses': address_serializer.data,
        })
