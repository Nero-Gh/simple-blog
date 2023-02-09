from django.urls import path
from . import views
from rest_framework_simplejwt.views import(
    TokenObtainPairView,TokenRefreshView,TokenVerifyView
)


urlpatterns = [
    path("register/",views.SignUpView.as_view(),name='register'),
    path("login/",views.LoginView.as_view(),name='login'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
