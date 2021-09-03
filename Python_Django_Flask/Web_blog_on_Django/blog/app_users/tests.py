from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Profile


TEST_USERNAME = 'test_user'
TEST_USER_PASSWORD = '1234'
USER_EMAIL = 'test@test.com'
OLD_PASSWORD = 'testpassword'


class UserTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        for news_index in range(5):
            Profile.objects.create(
                user=User.objects.create(username=f'test{news_index}', first_name='test1'),
                city='город',
            )

    def test_url_location(self):
        response = self.client.get(reverse('app_users:login'))
        self.assertEqual(response.status_code, 200)

    def test_correct_template(self):
        response = self.client.get(reverse('app_users:login'))
        self.assertTemplateUsed(response, 'app_users/login.html')

    def test_register_user(self):
        response = self.client.get(reverse('app_users:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(Profile.objects.all()) == 5)

    def test_update_user_info(self):
        user = User.objects.create_user(username=TEST_USERNAME, email=USER_EMAIL, password=TEST_USER_PASSWORD)
        user.save()
        user_profile = Profile.objects.create(user=user, city='city')
        user_profile.save()
        old_city = user_profile.city
        login = self.client.login(username=TEST_USERNAME, password=TEST_USER_PASSWORD)
        response_login = self.client.get(reverse('app_users:login'))
        self.assertEqual(str(response_login.context['user']), TEST_USERNAME)
        self.assertEqual(response_login.status_code, 200)

        response = self.client.post(reverse('app_users:edit', args=[str(user_profile.id)]), {'city': 'new_city'})
        self.assertEqual(response.status_code, 302)
        user_profile.refresh_from_db()
        self.assertNotEqual(old_city, user_profile.city)

    def test_correct_post_password(self):
        user = User.objects.create(username=TEST_USERNAME, email=USER_EMAIL)
        response = self.client.post(reverse('app_users:restore_password'), {'email': USER_EMAIL})
        self.assertEqual(response.status_code, 200)
        from django.core.mail import outbox
        self.assertEqual(len(outbox), 1)
        self.assertIn(USER_EMAIL, outbox[0].to)

    def test_password_changed(self):
        user = User.objects.create(username=TEST_USERNAME, email=USER_EMAIL)
        user.set_password(OLD_PASSWORD)
        user.save()
        old_password_hash = user.password
        response = self.client.post(reverse('app_users:restore_password'), {'email': USER_EMAIL})
        self.assertEqual(response.status_code, 200)
        user.refresh_from_db()
        self.assertNotEqual(old_password_hash, user.password)
