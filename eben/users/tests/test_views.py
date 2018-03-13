from rest_framework.test import APIClient, APIRequestFactory

from test_plus.test import TestCase

from ..views import (
    UserUpdateView
)


class BaseAPIUserTestCase(TestCase):
    client_class = APIClient

    def setUp(self):
        self.user = self.make_user()
        self.factory = APIRequestFactory()


class TestUserUpdateView(BaseAPIUserTestCase):

    def setUp(self):
        # call BaseUserTestCase.setUp()
        super(TestUserUpdateView, self).setUp()
        # Instantiate the view directly. Never do this outside a test!
        self.view = UserUpdateView()
        # Generate a fake request
        request = self.factory.get('/fake-url')
        # Attach the user to the request
        request.user = self.user
        # Attach the request to the view
        self.view.request = request

    def test_get_object(self):
        # Expect: self.user, as that is the request's user object
        self.view.kwargs = {'username': 'testuser'}
        self.assertEqual(
            self.view.get_object(),
            self.user
        )
