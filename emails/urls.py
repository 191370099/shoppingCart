from django.urls import path
from emails.views import SendEmailView

urlpatterns = [
    path('send-email/', SendEmailView.as_view(), name='send-email'),
]