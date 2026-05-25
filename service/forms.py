from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.db.models import BooleanField
from django.forms import ModelForm

from service.models import Newsletter, Message, Recipient


class StyleFormMixin:
    """Класс стилизации форм"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class NewsletterForm(StyleFormMixin, ModelForm):
    """Класс формы создания/изменения рассылки"""


    class Meta:
        model = Newsletter
        fields = ["start_time", "end_time", "message", "recipients"]

        widgets = {
            'start_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            'end_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
        }

    def clean_end_time(self):
        """Метод проверки корректности даты окончания"""
        start_time = self.cleaned_data.get("start_time")
        end_time = self.cleaned_data.get("end_time")

        if start_time and end_time:
            if end_time.timestamp() < start_time.timestamp():
                raise ValidationError("Дата окончания должна быть позже даты начала")
        return end_time


class MessageForm(StyleFormMixin, ModelForm):
    """Класс формы создания/изменения сообщения"""


    class Meta:
        model = Message
        fields = ["theme", "body"]


class RecipientForm(StyleFormMixin, ModelForm):
    """Класс формы создания/изменения клиентов"""


    class Meta:
        model = Recipient
        fields = ["email", "name", "comment"]
