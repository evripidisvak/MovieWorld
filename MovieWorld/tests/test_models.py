from django.test import TestCase

from movieworld.models import *
from model_bakery import baker


class MovieTestModel(TestCase):
    """
    Class to test the model Movie
    """

    def set_up(self):
        movie = baker.make("movieworld.Movie")
        return movie

    def test_movie_model_title(self):
        movie = self.set_up()
        self.assertTrue(isinstance(movie, Movie))
        self.assertEqual(str(movie), movie.title)


class OpinionTestModel(TestCase):
    """
    Class to test the model Opinion
    """

    def set_up(self):
        opinion = baker.make("movieworld.Opinion")
        return opinion

    def test_opinion_model_like(self):
        opinion = self.set_up()
        print(f"{opinion.like = }")
        self.assertTrue(isinstance(opinion, Opinion))
        self.assertEqual(str(opinion), str(opinion.like))
