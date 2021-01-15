from django.shortcuts import render,redirect
from.forms import *
from django.views.generic import *
from django.urls import reverse_lazy
import requests
from django.conf import settings



# Create your views here.
class RegistrationAPIView(FormView):
    template_name = "register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy('userapp:dashboard')

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
        # print(data)
        print(resp.json())
        if resp.json().get('fail'):
            return render(self.request,self.template_name,{'form':form,'error':'Email already exists.'})
        return super().form_valid(form)






class LoginAPIView(FormView):
    template_name = "signin.html"
    form_class = UserLoginForm
    success_url = reverse_lazy('userapp:dashboard')

    def form_valid(self, form):
        username = form.cleaned_data['username']

        password = form.cleaned_data['password']
        login_api = "http://127.0.0.1:8000/api/v1/get-token/"
        data = {
            'username': username,
            'password': password
        }

        try:
            resp = requests.post(url=login_api, data=data)
            resp_data = resp.json()
            # print('===============')
            # print(resp_data)
            if resp_data.get('token'):
                self.request.session['token'] = resp_data.get('token')
            else:
                return render(self.request, self.template_name, {'form': form, 'error': 'Invalid credentials'})
        except:
            return redirect("/")
        return super().form_valid(form)






class UserRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):

        # print( request.session.get('token'))
        try:
            if request.session.get('token'):
                token = "Token " + request.session.get('token')
                self.headers = {'Authorization': token}
                resp = requests.get('http://127.0.0.1:8000/api/v1/user-profile/', headers=self.headers)
                if 'user' in resp.json():

                    self.user = resp.json()['user']
                    self.user_id = resp.json()['user']['id']


                else:
                    return redirect('/user-login-from-api/?err=err')
            else:
                return redirect('userapp:loginapi')
        except:
            return redirect("/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.user_id
        context['user_name'] = self.user['username']

        return context





class LogoutAPIView(UserRequiredMixin,View):
    def get(self, request):
        del request.session['token']
        return redirect('userapp:home')



class NewsListView(TemplateView):

    template_name = 'news/home.html'



class DashboardView(UserRequiredMixin,TemplateView):

    template_name = 'dashboard.html'


class AggregatedNewsListView(UserRequiredMixin,TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        hedlines_api = "http://127.0.0.1:8000/api/v1/news-headlines/"
        hedlines = requests.get(hedlines_api)
        many_headlines = hedlines.json()

        topics_api = "http://127.0.0.1:8000/api/v1/topics/"
        topics = requests.get(topics_api)
        many_topics = topics.json()
        # print(many_topics[0]['subscriber'])
        print(many_topics)






        context = super().get_context_data(**kwargs)
        context['news_list'] = many_headlines
        context['topics'] = many_topics

        return context



class RefreshNewsView(View):
    def post(self,request,*args,**kwargs):
        url = "http://127.0.0.1:8000/api/v1/refresh-news/"
        response = requests.post(url)
        # print(response)

        return redirect("userapp:dashboard")


class UserSubscribeView(UserRequiredMixin,View):
    def post(self,request,*args,**kwargs):
        url = "http://127.0.0.1:8000/api/v1/user-topic-subscribe/"
        t = request.POST['topic_id']

        resp = requests.get('http://127.0.0.1:8000/api/v1/user-profile/', headers=self.headers)
        # print(resp.json()['user']['id'])

        data = {
            'topic_id':t,
            'user':resp.json()['user']['username']

        }

        response = requests.post(url,data=data)
        print(data)

        return redirect("userapp:dashboard")




class UserUnsubscribeView(UserRequiredMixin,View):
    def post(self,request,*args,**kwargs):
        url = "http://127.0.0.1:8000/api/v1/user-topic-unsubscribe/"
        t = request.POST['topic_id']

        resp = requests.get('http://127.0.0.1:8000/api/v1/user-profile/', headers=self.headers)
        # print(resp.json()['user']['id'])

        data = {
            'topic_id':t,
            'user':resp.json()['user']['username']

        }

        response = requests.post(url,data=data)
        print(data)

        return redirect("userapp:dashboard")
    pass





