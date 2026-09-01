import traceback
from django.core.cache import cache
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import Group

from service.forms import NewsletterForm, MessageForm, RecipientForm
from service.models import Newsletter, Message, Recipient
from service.services import start_maling
from users.models import User


class StartView(TemplateView):
    """Контролер для главной страницы (данные пользователя)"""

    template_name = "service/start_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_list = Newsletter.objects.all()
        context['newslette_all'] = len(list((newsletter for newsletter in object_list if newsletter.owner == self.request.user)))
        for newsletter in object_list:
            new_status = newsletter.update_status()
            newsletter.status = new_status
            newsletter.save()
        context['newslette_activ'] = len([newsletter for newsletter in object_list if newsletter.status == 'Запущена' and newsletter.owner == self.request.user])
        messege = Message.objects.all()
        context['message_all'] = len(list((sms for sms in messege if sms.owner == self.request.user)))
        recipients = Recipient.objects.all()
        context['recipient_all'] = len(list((recipient for recipient in recipients if recipient.owner == self.request.user)))
        object_list = User.objects.all()
        context['user_all'] = len([user for user in object_list if user.groups.filter(name='Пользователь').exists()])
        return context


class ListNewsletter(ListView):
    """Контролер создания списка рассылок"""
    model = Newsletter
    template_name = "service/send_list.html"


class NewsletterCreateView(CreateView):
    """Класс добавления рассылки"""

    model = Newsletter
    # Название формы
    template_name = "service/send_forms.html"
    # Какие поля будут в форме создания
    form_class = NewsletterForm
    # Куда перенаправляется после того как будет выполнено
    success_url = reverse_lazy("service:send_list")

    def form_valid(self, form):
        user = self.request.user
        form.instance.owner = user
        print(user.groups.all())
        #form.instance.owner_group = user.groups.all()[0].name
        return super().form_valid(form)

class NewsletterUpdateView(UpdateView):
    """Класс редактирования рассылки"""

    model = Newsletter
    template_name = "service/send_forms.html"
    form_class = NewsletterForm
    success_url = reverse_lazy("service:send_list")


class NewsletterDeleteView(DeleteView):
    """Класс удаления рассылки"""

    model = Newsletter
    success_url = reverse_lazy("service:send_list")


class StartMailingView(View):
    """Контроллер запуска рассылки"""

    def post(self, request, pk):
        mailing = get_object_or_404(Newsletter, id=pk)

        try:
            start_maling(mailing)
            mailing.save()
        except Exception as e:
            mailing.save()
            print(e)

        return redirect("service:send_list")


class ListMessage(ListView):
    """Контролер создания списка сообщений"""
    model = Message
    template_name = "service/message_list.html"


class MessageCreateView(CreateView):
    """Класс добавления сообщений"""

    model = Message
    template_name = "service/message_forms.html"
    form_class = MessageForm
    success_url = reverse_lazy("service:message_list")

    def form_valid(self, form):

        form.instance.owner = self.request.user

        return super().form_valid(form)

class MessageUpdateView(UpdateView):
    """Класс редактирования сообщений"""

    model = Message
    template_name = "service/message_forms.html"
    form_class =MessageForm
    success_url = reverse_lazy("service:message_list")


class MessageDeleteView(DeleteView):
    """Класс удаления сообщений"""

    model = Message
    success_url = reverse_lazy("service:message_list")

class ListRecipient(ListView):
    """Контролер создания списка клиентов"""

    model = Recipient
    template_name = "service/recipient_list.html"


class RecipientCreateView(CreateView):
    """Класс добавления клиентов"""

    model = Recipient
    template_name = "service/recipient_forms.html"
    form_class = RecipientForm
    success_url = reverse_lazy("service:recipient_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user

        return super().form_valid(form)

class RecipientUpdateView(UpdateView):
    """Класс редактирования клиентов"""

    model = Recipient
    template_name = "service/recipient_forms.html"
    form_class = RecipientForm
    success_url = reverse_lazy("service:recipient_list")


class RecipientDeleteView(DeleteView):
    """Класс удаления клиентов"""

    model = Recipient
    success_url = reverse_lazy("service:recipient_list")


class BlockUserView(LoginRequiredMixin, View):
    """Контроллер для блокировки пользователя"""

    def post(self, request, pk):
        newsletter = get_object_or_404(Newsletter, id=pk)
        user = get_object_or_404(User, id=newsletter.owner.pk)

        if not request.user.has_perm('user.can_block_user'):
            return HttpResponseForbidden("У вас нет прав для блокировки пользователя.")

        user.block_status = True
        user.save()
        return redirect("service:mod_send_list")

class DisconnectionNewsletterView(LoginRequiredMixin, View):
    """Контроллер для блокировки пользователя"""

    def post(self, request, pk):
        newsletter = get_object_or_404(Newsletter, id=pk)

        if not request.user.has_perm('service.can_activity_status'):
            return HttpResponseForbidden("У вас нет прав для блокировки пользователя.")


        newsletter.activity_status = False
        newsletter.save()

        return redirect("service:mod_send_list")


class ModeratorListNewsletter(ListView):
    """Контролер создания списка всех рассылок всех пользователей для модераторов"""
    model = Newsletter
    template_name = "service/mod_send_list.html"




class ListAllNewsletter(ListView):
    """Контролер создания списка всех клиентов для модераторов"""
    model = Recipient
    template_name = "service/all_recipient.html"

    def get_queryset(self):
        queryset = cache.get('all_recipient')
        if not queryset:
            queryset = super().get_queryset()
            cache.set('all_recipient', queryset, 60*5)
        return queryset
