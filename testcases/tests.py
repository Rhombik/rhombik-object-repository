

from django.test import TestCase
from django.test.client import Client

##built in sample test case. Useless.
class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

##We're mostly going to try and test things for a user functionality point of view. Test to make sure that url's still point to content, test to make sure the user can upload and delete files. All that.
##The actual code and the interfaces between apps are not that big, and they're a twisty maze of passages all alike. It's probably not worth it to test an app interface these days, but feel free to add a class that does that.
##Just don't be suprised if we ignore it in favour of UserView tests. A commit doesn't go live unless it passes every UserViewTest. Try not to test features that aren't required to UserViewTest.


class UserViewTest(TestCase):
  user="testuser"
  passw="testpass"
  #Defines the client session. We're mostly going to be doing this in order. Need to define a test dependency graph.
  client=Client()

  from userProfile.models import userProfile
  from django.contrib.auth.models import User


  def test_register(self):
    c = self.client
    c.post('/register/', {'username': self.user, 'password1': self.passw, 'password2': self.passw,})
    self.assertIn('_auth_user_id', c.session)
    self.assertEqual(self.User.objects.all()[0].username,self.user)

  def test_logout(self):
    c = self.client
    c.post('/logout/', {})
    self.assertNotIn('_auth_user_id', c.session)
  def test_login(self):
    c = self.client
    c.post('/login/', {'username': self.user, 'password': self.passw,})
    self.assertIn('_auth_user_id', c.session)

