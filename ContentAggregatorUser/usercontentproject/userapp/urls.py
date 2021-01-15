from django.urls import path

from userapp.views import *

app_name = 'userapp'
urlpatterns = [

  path('', NewsListView.as_view(), name="home"),
  path('dashboard/', AggregatedNewsListView.as_view(), name="dashboard"),
  path('user-register-from-api/', RegistrationAPIView.as_view(), name="registerapi"),
  path('user-login-from-api/', LoginAPIView.as_view(), name="loginapi"),
  path('user-logout-from-api/', LogoutAPIView.as_view(), name="logoutapi"),
  path('news-refresh/', RefreshNewsView.as_view(), name="refreshnews"),
  path('user-subscribe/', UserSubscribeView.as_view(), name="usersubscribe"),
  path('user-unsubscribe/', UserUnsubscribeView.as_view(), name="unsubscribe"),

  # api views
]