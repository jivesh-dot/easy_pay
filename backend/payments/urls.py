from django.urls import path
from .views import PaymentIntentView


urlpatterns = [
    path('payment-intents/', PaymentIntentView.as_view()),
    path('payment-intents/<str:pk>/', PaymentIntentView.as_view()),
]