from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from notification.smtp2gomailsender import send_email_via_smtp2go
from django.core.signing import TimestampSigner
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


def generate_verification_link(user, request):
    signer = TimestampSigner()
    token = signer.sign(user.pk)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    
    # Doğrulama bağlantısı
    #verification_url = f"{request.scheme}://{request.get_host()}/customerauth/user/verify/{uid}/{token}/"

    verification_url = f"http://localhost:3000/verify-email/{uid}/{token}/"
    return verification_url



def send_confirmation_email(user, request):
    confirmation_link = generate_verification_link(user, request)
    
    subject = 'E-posta Doğrulama'
    message = render_to_string('email_templates/confirmation_email.html', {
        'user': user,
        'confirmation_link': confirmation_link,
    })

    send_email_via_smtp2go([user.email], subject, message)


def send_email_change_notification(email, user, old_email):
    subject = 'E-posta Değişikliği'
    message = render_to_string('email_templates/change_email.html', {
        'user': user,
        'new_email': email,
        'old_email':old_email,
        "subject":subject
    })

    send_email_via_smtp2go([user.email], subject, message)



def send_welcome_email(user):
    subject = 'Hoş Geldiniz'
    message = render_to_string('email_templates/welcome_email.html', {
        'user': user,
        "subject":subject,
        "site_url":"https://esyala.com/"
    })

    send_email_via_smtp2go([user.email], subject, message)