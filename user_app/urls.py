from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RequestVerificationCodeView, ConfirmVerificationCodeView


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')



urlpatterns = [
    path('user_app/', include(router.urls)),
    path('verify/request/', RequestVerificationCodeView.as_view(), name='request-code'),
    path('verify/confirm/', ConfirmVerificationCodeView.as_view(), name='confirm-code'),
]