from django.utils import timezone

from django.db import models

from users.models import User



class Recipient(models.Model):
    """Модель получателя рассылки"""

    email = models.EmailField(unique=True, verbose_name="Email")
    name = models.CharField(max_length=100, verbose_name=" ФИО клиента", help_text="Укажите ФИО клиента")
    comment = models.TextField(verbose_name="Комментарий", blank=True, null=True, help_text="Введите комментарий")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Пользователь", blank=True, null=True)
    owner_group = models.CharField(max_length=100, verbose_name="Группа автора", default="Не указано")

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ['name']


    def __str__(self):
        return self.name


class Message(models.Model):
    """Модель сообщений"""

    theme = models.CharField(max_length=100, verbose_name="Тема письма", help_text="Укажите тему новости")
    body = models.TextField(verbose_name="Тело письма", blank=True, null=True, help_text="Здесь вы можете описать подробности вашей новости")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Пользователь", blank=True, null=True)
    owner_group = models.CharField(max_length=100, verbose_name="Группа автора", default="Не указано")

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ['theme']

    def __str__(self):
        return self.theme


class Newsletter(models.Model):
    """Модель управления рассылкой сообщений"""

    start_time = models.DateTimeField(verbose_name="Дата начала рассылки", help_text="Укажите дату и время начала рассылки в формате")
    end_time = models.DateTimeField(verbose_name="Дата окончания рассылки", help_text="Укажите дату и время окончания рассылки")
    status = models.CharField(max_length=100, verbose_name="Статус", default="Создана")
    message = models.ForeignKey(
        Message,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Сообщение",
        help_text="Укажите тему сообщения",
        related_name="messages",
    )
    recipients = models.ManyToManyField(Recipient, verbose_name="Клиенты рассылки", related_name="recipients")
    dispatch_status = models.CharField(max_length=100, verbose_name="Статус рассылки", default="Отправка не осуществлялась")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Пользователь", blank=True, null=True)
    activity_status = models.BooleanField(default=True, verbose_name="Статус включенности рассылки")
    owner_group =  models.CharField(max_length=100, verbose_name="Группа автора", default="Не указано")

    def update_status(self):
        date_time = timezone.now()
        if date_time.timestamp()  < self.start_time.timestamp():
            new_status = 'Создана'
        elif self.start_time.timestamp()  <= date_time.timestamp()  <= self.end_time.timestamp() :
            new_status = 'Запущена'
        else:
            new_status = 'Завершена'
        return new_status

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        permissions = [("can_activity_status", "Can activity status")]



