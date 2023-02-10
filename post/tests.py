from rest_framework.test import APITestCase, APIRequestFactory
from .views import PostListCreateView
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model


User = get_user_model()


class HelloWorldTestCase(APITestCase):
    def test_hello_world(self):
        response = self.client.get(reverse("posts_home")) #api endpoint

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Hello World")


class PostListCreateTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("list_posts")

    def authenticate(self):
        self.client.post(
            reverse("register"),
            {
                "email": "jvass@gmail.com",
                "password": "admin1234",
                "username": "jvass",
            },
        )

        response = self.client.post(
            reverse("login"),
            {
                "email": "kofi@gmail.com",
                "password": "admin1234",
            },
        )

        print(response.data)

        token = response.data["token"]["access"]

        self.client.credentials(HTTP_AUTHORIZATION = f"Bearer {token}")

    def test_list_posts(self): 

        response = self.client.get(self.url)


        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)
        self.assertEqual(response.data["results"], [])
        

    def test_post_creation(self):
        self.authenticate()

        sample_data = {"title": "Sample title", "description": "Sample content"}
        response = self.client.post(reverse("list_posts"), sample_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], sample_data["title"])
        
