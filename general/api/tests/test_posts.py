from rest_framework.test import APITestCase
from rest_framework import status
from general.models import Post
from general.factories import UserFactory, PostFactory
import json
from django.core.serializers.json import DjangoJSONEncoder


class PostTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

        self.url = "/api/posts/"
    
    # def _unauthorized_post_request(self, url, data):
    #     self.client.logout()

    #     response = self.client.post(
    #         path=url,
    #         data=data,
    #         format="json",
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #     self.assertEqual(Post.objects.all().count(), 0)
    
    # def _unauthorized_get_request(self, url):
    #     self.client.logout()

    #     response = self.client.get(path=url, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #     self.assertEqual("results" in response.data, False)

    def test_create_post(self):
        data = {
            "title": "some post title",
            "body": "some text",
        }
        response = self.client.post(
            path=self.url,
            data=data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        post = Post.objects.last()
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.title, data["title"])
        self.assertEqual(post.body, data["body"])
        self.assertIsNotNone(post.created_at)
    
    def test_unauthorized_post_request(self):
        self.client.logout()

        data = {
            "title": "some post title",
            "body": "some text",
        }
        response = self.client.post(
            path=self.url,
            data=data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Post.objects.all().count(), 0)

    def test_post_list(self):
        PostFactory.create_batch(5)

        response = self.client.get(path=self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 5)
    
    def test_post_list_data_structure(self):
        post = PostFactory()
        response = self.client.get(path=self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = json.loads(
            json.dumps(
                response.data["results"][0],
                cls=DjangoJSONEncoder,
            )
        )

        author = post.author
        expected_data = {
            "id": post.pk,
            "author": {
                "id": author.pk,
                "first_name": author.first_name,
                "last_name": author.last_name,
            },
            "title": post.title,
            "body": (
                post.body[:125] + "..."
                if len(post.body) > 128
                else post.body 
            ),
            "created_at": post.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
        }

        self.assertDictEqual(expected_data, response_data)
