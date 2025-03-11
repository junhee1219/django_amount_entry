from django.urls import path
from .views import LoginView, RegisterView, EmailVerifyView

urlpatterns = [
	path('login/', LoginView.as_view(), name='api-login'),
	path('register/', RegisterView.as_view(), name='api-register'),
	path('verify-email/', EmailVerifyView.as_view(), name='email-verify'),
]
