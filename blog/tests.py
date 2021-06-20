from django.test import TestCase, Client
from django.contrib.auth.models import User
from bs4 import BeautifulSoup
from .models import Post, Category, Tag


class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_obama = User.objects.create_user(username='obama', password='somepassword')
        self.user_trump = User.objects.create_user(username='trump', password='somepassword')

        self.category_life = Category.objects.create(name='life', slug='life')
        self.category_culture = Category.objects.create(name='culture', slug='culture')

        self.tag_python_kor = Tag.objects.create(name='파이썬 공부', slug='파이썬-공부')
        self.tag_python = Tag.objects.create(name='python', slug='python')
        self.tag_hello = Tag.objects.create(name='hello', slug='hello')

        self.post_001 = Post.objects.create(
            title='첫번째 포스트입니다',
            content='헬로 윌드, 위아더월드',
            category=self.category_life,
            author=self.user_obama
        )
        self.post_001.tags.add(self.tag_hello)

        self.post_002 = Post.objects.create(
            title='두번째 포스트입니다',
            content='1등이 전부는 아니잖아요?',
            category=self.category_culture,
            author=self.user_trump
        )
        self.post_003 = Post.objects.create(
            title='세번째 포스트입니다',
            content='3등이어도 괜찮아요',
            author=self.user_trump
        )
        self.post_003.tags.add(self.tag_python_kor)
        self.post_003.tags.add(self.tag_python)

    def navbar_tast(self, soup):
        navber = soup.nav
        self.assertIn('Blog', navber.text)
        self.assertIn('About me', navber.text)

        logo_btn = navber.find('a', text='wishty')
        self.assertEqual(logo_btn.attrs['href'], '/')

        home_btn = navber.find('a', text='Home')
        self.assertEqual(home_btn.attrs['href'], '/')

        blog_btn = navber.find('a', text='Blog')
        self.assertEqual(blog_btn.attrs['href'], '/blog/')

        about_me_btn = navber.find('a', text='About me')
        self.assertEqual(about_me_btn.attrs['href'], '/about_me/')

    def category_card_test(self, soup):
        categories_card = soup.find('div', id='categories-card')
        self.assertIn('Categories', categories_card.text)
        self.assertIn(f'{self.category_life.name} ({self.category_life.post_set.count()})', categories_card.text)
        self.assertIn(f'{self.category_culture.name} ({self.category_culture.post_set.count()})', categories_card.text)
        self.assertIn(f'미분류 (1)', categories_card.text)

    def test_post_list(self):
        # 포스트가 있는 경우
        self.assertEqual(Post.objects.count(), 3)

        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.navbar_tast(soup)
        self.category_card_test(soup)

        main_area = soup.find('div', id='main-area')
        self.assertNotIn('아직 게시물이 없습니다', main_area.text)

        post_001_card = main_area.find('div', id='post-1')
        self.assertIn(self.post_001.title, post_001_card.text)
        self.assertIn(self.post_001.category.name, post_001_card.text)
        self.assertIn(self.tag_hello.name, post_001_card.text)
        self.assertNotIn(self.tag_python.name, post_001_card.text)
        self.assertNotIn(self.tag_python_kor.name, post_001_card.text)

        post_002_card = main_area.find('div', id='post-2')
        self.assertIn(self.post_002.title, post_002_card.text)
        self.assertIn(self.post_002.category.name, post_002_card.text)
        self.assertNotIn(self.tag_hello.name, post_002_card.text)
        self.assertNotIn(self.tag_python.name, post_002_card.text)
        self.assertNotIn(self.tag_python_kor.name, post_002_card.text)

        post_003_card = main_area.find('div', id='post-3')
        self.assertIn(self.post_003.title, post_003_card.text)
        self.assertIn('미분류', post_003_card.text)
        self.assertNotIn(self.tag_hello.name, post_003_card.text)
        self.assertIn(self.tag_python.name, post_003_card.text)
        self.assertIn(self.tag_python_kor.name, post_003_card.text)

        self.assertIn(self.user_obama.username.upper(), main_area.text)
        self.assertIn(self.user_trump.username.upper(), main_area.text)

        # 포스트가 없는 경우
        Post.objects.all().delete()
        self.assertEqual(Post.objects.count(), 0)

        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.navbar_tast(soup)

        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다', main_area.text)

    def test_post_detail(self):
        self.assertEqual(self.post_001.get_absolute_url(), '/blog/1/')

        resource = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(resource.status_code, 200)
        soup = BeautifulSoup(resource.content, 'html.parser')

        self.navbar_tast(soup)
        self.category_card_test(soup)

        self.assertIn(self.post_001.title, soup.title.text)

        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(self.post_001.title, post_area.text)

        self.assertIn(self.tag_hello.name, post_area.text)
        self.assertNotIn(self.tag_python.name, post_area.text)
        self.assertNotIn(self.tag_python_kor.name, post_area.text)

        self.assertIn(self.user_obama.username.upper(), post_area.text)

        self.assertIn(self.post_001.content, post_area.text)

    def test_category_page(self):
        response = self.client.get(self.category_life.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        self.navbar_tast(soup)
        self.category_card_test(soup)

        self.assertIn(self.category_life.name, soup.h1.text)

        main_area = soup.find('div', id='main-area')
        self.assertIn(self.category_life.name, main_area.text)
        self.assertIn(self.post_001.title, main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertNotIn(self.post_003.title, main_area.text)

    def test_tag_page(self):
        response = self.client.get(self.tag_hello.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.navbar_tast(soup)
        self.category_card_test(soup)

        self.assertIn(self.tag_hello.name, soup.h1.text)

        main_area = soup.find('div', id='main-area')
        self.assertIn(self.tag_hello.name, main_area.text)
        self.assertIn(self.post_001.title, main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertNotIn(self.post_003.title, main_area.text)
