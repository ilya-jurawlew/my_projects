from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import News, Comments


TEST_USERNAME = 'test'
TEST_USER_PASSWORD = '1234'
USER_EMAIL = 'email@email.com'
TEST_COMMENT = 'здесь находится коммент'


class NewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        for news_index in range(10):
            News.objects.create(
                title='привет',
                content='мир',
                activity=True
            )

        Comments.objects.create(
            text=TEST_COMMENT,
            news=News.objects.get(id=1)
        )

    def test_url_location(self):
        response = self.client.get(reverse('app_news:list'))
        self.assertEqual(response.status_code, 200)

    def test_correct_template(self):
        response = self.client.get(reverse('app_news:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, f'app_news/news_list.html')

    def test_create_news(self):
        response = self.client.get(reverse('app_news:list'))
        self.assertTrue(response.context['object_list'].count() == 10)

    def test_update_news(self):
        user = User.objects.create_superuser(username=TEST_USERNAME, email=USER_EMAIL, password=TEST_USER_PASSWORD)
        user.save()
        news = News.objects.create(title='привет', content='мир')
        news.save()
        old_content = news.content
        login = self.client.login(username=TEST_USERNAME, password=TEST_USER_PASSWORD)
        response = self.client.post(reverse('app_news:edit', args=[str(news.id)]), {'content': 'миру мир'})
        self.assertEqual(response.status_code, 302)
        news.refresh_from_db()
        self.assertNotEqual(old_content, news.content)

    def test_create_comments(self):
        response = self.client.get(reverse('app_news:detail', args=[str(1)]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, TEST_COMMENT)
