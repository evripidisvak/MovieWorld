from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Movie(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    # class Meta:
    #     verbose_name = _("movie")
    #     verbose_name_plural = _("movies")

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse("movie_detail", kwargs={"pk": self.pk})


class Opinion(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.BooleanField()

    # class Meta:
    #     verbose_name = _("Opinion")
    #     verbose_name_plural = _("Opinions")

    def __str__(self):
        return str(self.like)
