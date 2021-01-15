from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .models import *
from rest_framework.generics import *
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render,redirect
from bs4 import BeautifulSoup
from django.views.generic import *
import requests
from django.http import HttpResponse


class HeadlinesViewset(viewsets.ModelViewSet):
    queryset = Headline.objects.all()
    serializer_class = HeadlineSerializer


class HeadlinesListAPIView(ListAPIView):
    queryset = Headline.objects.all()
    serializer_class = HeadlineSerializer


class TopicListAPIView(ListAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


class UserRegistrationAPIView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PartnerUserProfileView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            user = request.user
            return Response({'user': ProfileSerializer(user).data})
        except:
            return Response({'error': 'Unidentified user'})



class AggregrateAPIView(APIView):

    def post(self,request):
      """gadgets and tech news"""
      url1 = "https://www.gadgetbytenepal.com/blog-news-list/"

      content1 = requests.get(url1, verify=False).content
      soup1 = BeautifulSoup(content1,features="html.parser")
      News1 = soup1.find_all('div', {"class":"td_module_10"})


      for news in News1:
          main = news.find('a')

          link1 = main['href']

          image_src = str(main.find('img')['data-img-url'])

          newsheadline = Headline()

          title = main['title']

          newstopic = Topic.objects.get(title='Tech and Gadgets')

          newsheadline.topic = newstopic
          newsheadline.title = title
          newsheadline.url = link1
          newsheadline.image = image_src
          if not Headline.objects.filter(title=title).exists():
              newsheadline.save()



      """Political news"""
      url2 = "https://kathmandupost.com/politics"

      content2 = requests.get(url2, verify=False).content
      soup2 = BeautifulSoup(content2, features="html.parser")

      News2 = soup2.find_all('article', {"class":"article-image"})


      for news in News2[:10]:
          main = news.find_all('a')[0]

          link2 = "https://kathmandupost.com/"+ main['href']

          image_src = str(main.find('img')['data-src'])
          # print(image_src)
          start = '<h3>'
          end = '</h3>'
          s = str(news.find('h3'))
          title = (s[s.find(start) + len(start):s.rfind(end)])


          newsheadline = Headline()
          newstopic = Topic.objects.get(title='Politics')
          newsheadline.topic = newstopic
          newsheadline.title = title
          newsheadline.url = link2
          newsheadline.image = image_src

          if not Headline.objects.filter(title=title).exists():
              newsheadline.save()



      return redirect("/")



class UserTopicSubscribeAPIView(View):


   def post(self, request, *args, **kwargs):
       # print("====")
       # print(request.POST['topic_id'])
       topic_id = request.POST['topic_id']
       user = request.POST['user']

       u = User.objects.get(username=user)

       topic = Topic.objects.get(id=topic_id)
       print('----===----')
       print(u)

       if not Subscription.objects.filter(user=u).exists():
           subscriber  = Subscription.objects.create(user=u)

           subscriber.topic.set([topic])

           subscriber.save()

           topic.subscriber.set([u])

           topic.save()
       else:
           user = Subscription.objects.get(user=u)
           user.topic.add(topic)
           user.save()
           topic.subscriber.set([u])
           topic.save()


       return redirect('Newsapp:home')




class UnSubscribeAPIView(View):

    def post(self, request, *args, **kwargs):

        user = request.POST['user']

        u = User.objects.get(username=user)



        topic_id = request.POST['topic_id']
        # user = request.POST['user']



        topic = Topic.objects.get(id=topic_id)
        print(u,topic_id)

        if Topic.objects.filter(subscriber=u).exists():
            topic = Topic.objects.get(id=topic_id)

            topic.subscriber.remove(u)

            topic.save()
        else:
            return HttpResponse('You have not subscribed yet!')

        return redirect('Newsapp:home')