from django.core.mail import send_mail
from django.conf import settings



def start_maling(newsletter):
    recipients = newsletter.recipients.all()
    list_emails = [recipient.email for recipient in recipients if recipient.email]

    if len(list_emails) > 0:
        try:
            result = send_mail(
                subject=newsletter.message.theme,
                message=newsletter.message.body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=list_emails,
                fail_silently=False,
            )
            if result > 0:
                newsletter.dispatch_status = 'Успешно выполнена'
                newsletter.save()
            else:
                newsletter.dispatch_status = 'Не успешно'
                newsletter.save()
        except Exception as e:
            newsletter.dispatch_status = f'Не успешно. Ошибка: {e}'
            newsletter.save()
    else:
        newsletter.dispatch_status = 'Не успешно.Список получателей пуст.'
        newsletter.save()
