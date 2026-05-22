from django.shortcuts import render
from django.views.generic import ListView

from service.models import Newsletter, Message, Recipient


class StartView(ListView):
    """Контролер для главной страницы (список товаров)"""

    model = Newsletter

    def get_context_data(self):
        # Добавляем свои собственные данные в контекст шаблона
        context = super().get_context_data()
        object_list = Newsletter.objects.all()
        context['newslette_all'] = len(list((newsletter for newsletter in object_list)))
        context['newslette_activ'] = len(list((newsletter for newsletter in object_list if newsletter.status == 'Запущена')))
        messege = Message.objects.all()
        context['message_all'] = len(list((sms for sms in messege)))
        recipients = Recipient.objects.all()
        context['recipient_all'] = len(list((recipient for recipient in recipients)))

        return context