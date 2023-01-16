from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post, Station
from django.contrib import messages
import requests

TIMEOUT = 5
PAGINATION = 10


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'termos/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'termos/home.html'  
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = PAGINATION


class UserPostListView(ListView):
    model = Post
    template_name = 'termos/user_posts.html'
    context_object_name = 'posts'
    paginate_by = PAGINATION

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')  


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['stations']

    def get_meteostat(self, request_params):
        url = request_params['url']
        response = {'msg': f"Cтанция {url} недоступна. Поробуйте еще раз", 'code': 0}
        try:
            r = requests.get(url, timeout=TIMEOUT)
            if r.status_code == 200:
                response['msg'] = r.json()
                response['code'] = 1
        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.ConnectTimeout:
            pass
        except requests.exceptions.ConnectionError:
            response['msg'] = f"Cтанция {url} выключена."

        return response

    def form_valid(self, form):
        form.instance.author = self.request.user

        #url = post.station_form form.instance.stations

        req_params = {"url": form.instance.stations.address, "params": []}

        resp = self.get_meteostat(req_params)
        if resp['code'] == 0:
            messages.error(self.request, resp['msg'])
            return super().form_invalid(form)
        else:
            #form.instance.title = f"Станция {form.instance.stations}"

            # noinspection PyTypeChecker
            res_content = f"Станция - {form.instance.stations}\n\n"\
                          f"Температура: {resp['msg']['temperature']}\n" \
                          f"Влажность: {resp['msg']['humidity']}\n" \
                          f"Направление ветра: {resp['msg']['windDirection']}\n" \
                          f"Скорость ветра: {resp['msg']['windSpeed']}\n" \
                          f"Мелкие частицы: {resp['msg']['pm2.5']}\n" \
                          f"pm5: {resp['msg']['pm5']}"

            form.instance.content = res_content

            return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'termos/about.html', {'title': 'Meteostation Web'})
