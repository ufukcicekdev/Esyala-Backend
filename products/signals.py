from django.db.models.signals import post_save
from django.dispatch import receiver

from notification.smtp2gomailsender import send_email_via_smtp2go
from slack_send_messages.send_messages import send_new_questions_message
from .models import Answer, Question
from django.template.loader import render_to_string


@receiver(post_save, sender=Answer)
def update_question_is_answered(sender, instance, created, **kwargs):
    if created:
        question = instance.question
        question.is_answered = True
        question.save()
        
        # E-posta bilgileri
        user = question.user  
        subject = 'Sorunuz Cevaplandı!'
        message = render_to_string('email_templates/answer.html', {
            'user': user.username,
            'question_text': question.question_text,
            'answer_text': instance.answer_text,
            'product_name': question.product.name,
            "subject":subject
        })
        
        send_email_via_smtp2go([user.email], subject, message)



@receiver(post_save, sender=Question)
def send_questions_message(sender, instance, created, **kwargs):
    if created:
        product = instance.product.name
        user = instance.user  
        question_text = instance.question_text 
        
     
        message = (
            f"Yeni bir soru oluşturuldu!\n"
            f"Ürün: {product}\n" 
            f"Kullanıcı: {user.username}\n"  
            f"Soru: {question_text}"
        )
        send_new_questions_message(message)
