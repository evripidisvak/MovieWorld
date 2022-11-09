from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count, F, Q, Subquery, OuterRef
from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
import pandas as pd

from .forms import *
from .models import *


class Index(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)

        param_dict = self.request.GET.dict()
        user_filter = None
        sort = None

        if param_dict:
            if "u" in param_dict.keys():
                user_filter = param_dict["u"]
            if "s" in param_dict.keys():
                sort = param_dict["s"]

        user = self.request.user

        movies = Movie.objects.all().annotate(
            likes=Count("opinion", filter=Q(opinion__like=True)),
            hates=Count("opinion", filter=Q(opinion__like=False)),
            user_opinion=Subquery(
                Opinion.objects.filter(
                    user__id=user.id, movie__id=OuterRef("id")
                ).values("like")
            ),
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
        user = request.user
        vote_type = request.POST.get("vote_type")
        movie_id = request.POST.get("movie_id")
        print(f"{movie_id = }")

        if vote_type == "like":
            vote = True
        else:
            vote = False

        # Get user opinion on the movie if it exists
        try:
            opinion = Opinion.objects.get(movie__id=movie_id, user=user)
        except:
            opinion = None

        # Update, create or delete user opinion
        if opinion is None or (opinion is not None and opinion.like != vote):
            opinion, created = Opinion.objects.update_or_create(
                movie=Movie.objects.get(id=movie_id), user=user, defaults={"like": vote}
            )
            modification = "created" if created else "toggled"
            current_opinion = opinion.like
        else:
            opinion.delete()
            modification = "deleted"
            current_opinion = None

        movie_opinions = Opinion.objects.filter(movie__id=movie_id)

        movie_opinions_df = pd.DataFrame.from_records(
            movie_opinions.values(), columns=["id", "movie_id", "user_id", "like"]
        )
        counts = movie_opinions_df["like"].value_counts()

        response_data = {}
        response_data["movie_id"] = movie_id
        response_data["likes_count"] = str(counts.get(True, 0))
        response_data["hates_count"] = str(counts.get(False, 0))
        response_data["modification"] = modification
        response_data["current_opinion"] = current_opinion

        return JsonResponse(response_data, safe=False)
