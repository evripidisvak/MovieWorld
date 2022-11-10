from http import client
from itertools import product
from urllib import response
from django.test import TestCase, SimpleTestCase, Client
from django.contrib.auth.models import AnonymousUser
from MovieWorld.urls import *
from django.urls import reverse
from django.contrib.auth.models import User
from model_bakery import baker
from movieworld.models import *


def login_dummy_user():
    client = Client()
    user = User.objects.create(username="testuser")
    user.set_password("12345")
    user.save()
    client.login(username="testuser", password="12345")
    return client


class TestLoginView(TestCase, SimpleTestCase):
    def setup(self):
        pass

    def test_login_success_and_fail(self):
        user = User.objects.create(username="testuser")
        user.set_password("12345")
        user.save()
        client = Client()
        logged_out = client.login(username="WRONGuser", password="WRONGpasswd")
        logged_in = client.login(username="testuser", password="12345")
        self.assertFalse(logged_out)
        self.assertTrue(logged_in)


class TestIndexView(TestCase, SimpleTestCase):
    def test_index_has_data(self):
        client = login_dummy_user()
        response = client.get(reverse("index"))
        self.assertTrue(response.status_code, 200)

    def test_index_has_movies(self):
        client = login_dummy_user()
        movie = baker.make("movieworld.Movie", _quantity=5)
        response = client.get(reverse("index"))
        self.assertTrue(response.status_code, 200)


class TestRegisterView(TestCase, SimpleTestCase):
    def test_index_has_data(self):
        client = Client()
        response = client.get(reverse("register"))
        self.assertTrue(response.status_code, 200)


class TestMovieCreateView(TestCase, SimpleTestCase):
    def test_index_has_data(self):
        client = login_dummy_user()
        response = client.get(reverse("add_movie"))
        self.assertTrue(response.status_code, 200)
