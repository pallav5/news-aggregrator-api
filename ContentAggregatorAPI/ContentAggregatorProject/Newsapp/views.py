import requests

from django.shortcuts import render,redirect
from bs4 import BeautifulSoup
from django.views.generic import *
from Newsapp.models import *
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate,logout

class AggregrateView(View):

    def get(self,request):
      """gadgets and tech news"""
      url1 = "https://www.gadgetbytenepal.com/blog-news-list/"

      content1 = requests.get(url1, verify=False).content
      soup1 = BeautifulSoup(content1,features="html.parser")
      News1 = soup1.find_all('div', {"class":"td_module_10"})


      for news in News1:
          main = news.find('a')

          link1 = main['href']

          image_src = str(main.find('img')['data-img-url'])

          title = main['title']


          newsheadline = Headline()
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






class UserRegisterVIew(CreateView):


    def get(self, request, *args, **kwargs):
        context = {
            'form': UserRegisterForm()
        }


        return render(request,'register.html',context)

    def post(self, request, *args, **kwargs):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            user = User.objects.create(username=username,email=email,password=password)
            if User.objects.filter(email=email).exists():
                user.save()
            else:
                return render(self.request, self.template_name, {
                    'form': form,
                    'error': 'User  already exists'
                })

            return redirect('/')
        return render (request,'register.html',{'form':form})


class LoginView(FormView):
    template_name = "signin.html"
    form_class = UserLoginForm
    success_url = reverse_lazy("Newsapp:home")

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        # print(email,password)
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None :
            login(self.request, user)
        else:

            return render(self.request, self.template_name, {
                'form': form,
                'error': 'Invalid credentials'
            })

        return super().form_valid(form)

    def get_success_url(self):
        if 'next' in self.request.GET:
            return self.request.GET['next']
        else:
            return self.success_url



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['loginform'] = UserLoginForm
        context['registrationform'] = UserRegisterForm
        return context




class LoginRequiredMixin(object):
    def dispatch(self, request, *args, ** kwargs):
        if request.user.is_authenticated:
            pass
        else:
            return redirect('/user-login/?next' + request.path)
        return super().dispatch(request, *args, **kwargs)


class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect("Newsapp:login")



class NewsListView(LoginRequiredMixin,TemplateView):

    template_name = 'news/home.html'



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # exists = self.request.GET.get('topic')
        # print(exists)
        # if Subscription.objects.filter(topic__title=exists):
        #     context['exists'] = 'exists'

        context['object_list'] = Headline.objects.all()
        context['Subscriber'] = Subscription.objects.all()
        context['Topics'] = Topic.objects.all()

        return context


from django.http import HttpResponse
class UserTopicSubscribe(View):


   def post(self, request, *args, **kwargs):
       topic_id = request.POST['topic']
       # print('====================')
       # print(topic_id)
       topic = Topic.objects.get(id=topic_id)
       print(request.user)

       if not Subscription.objects.filter(user=request.user).exists():
           subscriber = Subscription.objects.create(user=request.user)


           subscriber.topic.set([topic])

           subscriber.save()


           topic.subscriber.set([request.user])

           topic.save()
       else:
           user = Subscription.objects.get(user=request.user)
           user.topic.add(topic)
           user.save()
           topic.subscriber.set([request.user])
           topic.save()

       # if Subscription.objects.filter(topic=topic).exists():
       #
       #     return redirect('/?topic='+str(topic))

       return redirect('Newsapp:home')






class RegistrationAPIView(FormView):
    template_name = "register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy('Newsapp:home')

    def form_valid(self, form):
        registration_api = "http://127.0.0.1:8000/api/v1/user-registration/"
        username = form.cleaned_data["username"]

        email = form.cleaned_data["email"]
        password1 = form.cleaned_data["password1"]
        password2 = form.cleaned_data["password2"]

        data = {'email':email,
                'password1':password1,
                'password2':password2,
                'username':username,
                }

        resp = requests.post(registration_api,data=data)
        print("=======")
        print(data)
        print(resp.json())
        if resp.json().get('fail'):
            return render(self.request,self.template_name,{'form':form,'error':'Email already exists.'})
        return super().form_valid(form)




class LoginAPIView(FormView):
    template_name = "signin.html"
    form_class = UserLoginForm
    success_url = reverse_lazy('Newsapp:home')

    def form_valid(self, form):
        username = form.cleaned_data['username']

        password = form.cleaned_data['password']
        login_api = "http://127.0.0.1:8000/api/v1/get-token/"
        data = {
            'username': username,
            'password': password
        }
        # print(d)
        try:
            resp = requests.post(url=login_api, data=data)
            resp_data = resp.json()
            print('===============')
            print(resp_data)
            if resp_data.get('token'):
                self.request.session['token'] = resp_data.get('token')
            else:
                return render(self.request, self.template_name, {'form': form, 'error': 'Invalid credentials'})
        except:
            return redirect("/")
        return super().form_valid(form)



class LogoutAPIView(View):
    def get(self, request):
        del request.session['token']
        return redirect('Newsapp:home')






class UnSubscribeView(View):


   def post(self, request, *args, **kwargs):
       # print("====")
       # print(request.POST['topic_id'])
       topic_id = request.POST['topic']
       # user = request.POST['user']

       u = User.objects.get(username=self.request.user)

       topic = Topic.objects.get(id=topic_id)
       print(u)

       if Topic.objects.filter(subscriber=self.request.user).exists():
           topic = Topic.objects.get(id=topic_id)

           topic.subscriber.remove(self.request.user)


           topic.save()
       else:
           return HttpResponse('You have not subscribed yet!')



       return redirect('Newsapp:home')