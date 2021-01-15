"""ContentAggregatorProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers
from Newsapp.apiviews import *
router = routers.DefaultRouter()
router.register('headlines',HeadlinesViewset)
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/headlines-news/', HeadlinesListAPIView.as_view(),name = 'headlinelistapi'),
    path('api/v1/topics/', TopicListAPIView.as_view(),name = 'topiclistapi'),
    path('api/v1/user-profile/', PartnerUserProfileView.as_view(), name="partneruserprofile"),
    path('api/v1/user-registration/',UserRegistrationAPIView.as_view(), name="userregistrationapi"),
    path('api/v1/news-headlines/', HeadlinesListAPIView.as_view(), name="headlineslistapi"),
    path('api/v1/get-token/', obtain_auth_token, name='api_token_auth'),
    path('api/v1/refresh-news/', AggregrateAPIView.as_view(),name = 'aggregateapi'),
    path('api/v1/user-topic-subscribe/', csrf_exempt(UserTopicSubscribeAPIView.as_view()),name = 'usersubscriberapi'),
    path('api/v1/user-topic-unsubscribe/', csrf_exempt(UnSubscribeAPIView.as_view()),name = 'userunsubscriberapi'),
    path('',include('Newsapp.urls')),
    path('newsapi/',include(router.urls)),
    path('api-auth/', include('rest_framework.urls'))
]
