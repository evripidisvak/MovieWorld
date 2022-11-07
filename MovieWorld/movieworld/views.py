from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count, F, Q, Subquery
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from .forms import *
from .models import *


class Index(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        # print(f"{self.request.get_full_path() = }")
        # print(f"{self.request.GET.dict() = }")
        # print(f"{kwargs = }")

        param_dict = self.request.GET.dict()
        # print(f"{param_dict = }")
        user_filter = None
        sort = None

        if param_dict:
            if "u" in param_dict.keys():
                user_filter = param_dict["u"]
            if "s" in param_dict.keys():
                sort = param_dict["s"]
        # print(f"{user_filter = }")
        user = self.request.user
        # print(f"{sort = }")
        # print(f"{user_filter = }")

        movies = Movie.objects.all().annotate(
            likes=Count("opinion", filter=Q(opinion__like=True)),
            hates=Count("opinion", filter=Q(opinion__like=False)),
        )

        if user_filter is not None:
            movies = movies.filter(user=user_filter)

        if sort is not None:
            if sort == "l":  # sort by likes
                movies = movies.order_by("-likes")
            if sort == "h":  # sort by hates
                movies = movies.order_by("-hates")
            if sort == "d":  # sort by date
                movies = movies.order_by("-date")

        movies_count = len(movies)

        user_opinions = Opinion.objects.filter(user=user.id)
        for opinion in user_opinions:
            try:
                tmp = movies.get(id=opinion.movie_id)
                tmp.user_opinion = opinion.like
            except:
                pass

        context.update(
            {
                "user": user,
                "movies": movies,
                "movie_count": movies_count,
                "sort": sort,
                "user_filter": user_filter,
                "request": self.request,
            }
        )

        return context


# def logout_view(request):
#     logout(request)
#     return HttpResponseRedirect(settings.LOGIN_URL)


# def login_view(request):
#     login(request)
#     return HttpResponseRedirect(settings.LOGIN_URL)


# def register_view(request):
#     login(request)
#     return HttpResponseRedirect(settings.LOGIN_URL)


class Register(CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy("login")
    template_name = "registration/register.html"


class MovieCreateView(CreateView):
    model = Movie
    fields = ["title", "description"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("index")


def movie_vote(request):
    if request.method == "POST":
        print(f"{request.POST = }")
