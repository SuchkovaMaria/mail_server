from django.urls import path
from django.views.decorators.cache import cache_page
from service.apps import ServiceConfig
from service.views import StartView, ListNewsletter, StartMailingView, NewsletterCreateView, NewsletterUpdateView, \
    NewsletterDeleteView, ListMessage, MessageCreateView, MessageUpdateView, MessageDeleteView, ListRecipient, \
    RecipientCreateView, RecipientUpdateView, RecipientDeleteView, BlockUserView, DisconnectionNewsletterView, \
    ModeratorListNewsletter, ListAllNewsletter

app_name = ServiceConfig.name

urlpatterns = [
    path("", StartView.as_view(), name="home"),
    path("service/send_list", cache_page(60)(ListNewsletter.as_view()), name="send_list"),
    path("send/<int:pk>/start", StartMailingView.as_view(), name="start_mailing"),
    path("service/create/", NewsletterCreateView.as_view(), name="newsletter_create"),
    path("service/<int:pk>/update/", NewsletterUpdateView.as_view(), name="newsletter_update"),
    path("service/<int:pk>/delete/", NewsletterDeleteView.as_view(), name="newsletter_delete"),
    path("service/message_list", cache_page(60)(ListMessage.as_view()), name="message_list"),
    path("service/message_create/", MessageCreateView.as_view(), name="message_create"),
    path("service/<int:pk>/message_update/", MessageUpdateView.as_view(), name="message_update"),
    path("service/<int:pk>/message_delete/", MessageDeleteView.as_view(), name="message_delete"),
    path("service/recipient_list", cache_page(60)(ListRecipient.as_view()), name="recipient_list"),
    path("service/recipient_create/", RecipientCreateView.as_view(), name="recipient_create"),
    path("service/<int:pk>/recipient_update/", RecipientUpdateView.as_view(), name="recipient_update"),
    path("service/<int:pk>/recipient_delete/", RecipientDeleteView.as_view(), name="recipient_delete"),
    path("service/<int:pk>/block_user/", BlockUserView.as_view(), name="block_user"),
    path("service/<int:pk>/disconnect/", DisconnectionNewsletterView.as_view(), name="disconnect"),
    path("service/mod_send_list", cache_page(60)(ModeratorListNewsletter.as_view()), name="mod_send_list"),
    path("service/all_recipient_list", ListAllNewsletter.as_view(), name="all_recipient_list"),
]