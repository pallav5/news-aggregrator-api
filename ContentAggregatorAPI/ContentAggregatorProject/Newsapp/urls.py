from django.urls import path
from Newsapp.views import *
from Newsapp.apiviews import *

app_name = 'Newsapp'
urlpatterns = [
  path('aggregrate/', AggregrateView.as_view(), name="aggregrate"),
  path('', NewsListView.as_view(), name="home"),


  path('user-register/', UserRegisterVIew.as_view(), name="register"),
  path('user-login/', LoginView.as_view(), name="login"),
  path('logout/', LogoutView.as_view(), name="logout"),
  path('subscribe/', UserTopicSubscribe.as_view(), name="subscribe"),
  path('unsubscribe/', UnSubscribeView.as_view(), name="unsubscribe"),
  # path('user-register-from-api/', RegistrationAPIView.as_view(), name="registerapi"),
  # path('user-login-from-api/', LoginAPIView.as_view(), name="loginapi"),
  # path('user-logout-from-api/', LogoutAPIView.as_view(), name="logoutapi"),

  # api views
]