from django.test import TestCase, Client
from django.contrib.auth.models import User
from bs4 import BeautifulSoup
from .models import Post, Category


class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_obama = User.objects.create_user(username='obama', password='somepassword')
        self.user_trump = User.objects.create_user(username='trump', password='somepassword')

        self.category_life = Category.objects.create(name='life', slug='life')
        self.category_culture = Category.objects.create(name='culture', slug='culture')

        self.post_001 = Post.objects.create(
            title='첫번째 포스트입니다',
            content='헬로 윌드, 위아더월드',
            category=self.category_life,
            author=self.user_obama
        )
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

        post_002_card = main_area.find('div', id='post-2')
        self.assertIn(self.post_002.title, post_002_card.text)
        self.assertIn(self.post_002.category.name, post_002_card.text)

        post_003_card = main_area.find('div', id='post-3')
        self.assertIn(self.post_003.title, post_003_card.text)
        self.assertIn('미분류', post_003_card.text)

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
        # 1.1 포스트가 하나 있다.
        post_001 = Post.objects.create(
            title='첫번째 포스트입니다',
            content='헬로 월드, 위아더 월드',
            author=self.user_obama
        )
        # 1.2 포스트의 ulr은 '/blog/1/'이다.
        self.assertEqual(post_001.get_absolute_url(), '/blog/1/')

        # 2. 첫 번째 포스트의 상세 페이지 테스트
        # 2.1 첫 번째 포스트의 url로 접근하면 정상적으로 작동한다.
        resource = self.client.get(post_001.get_absolute_url())
        self.assertEqual(resource.status_code, 200)
        soup = BeautifulSoup(resource.content, 'html.parser')
        # 2.2 내비게이션 바가 있고 Blog, About Me라는 문구가 내비게이션 바에 있다.
        self.navbar_tast(soup)

        # 2.3 첫 번째 포스트의 제목이 웹 브라우저 탭 타이틀에 들어 있다.
        self.assertIn(post_001.title, soup.title.text)

        # 2.4 첫 번째 포스트의 제목이 포스트 영역에 있다.
        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(post_001.title, post_area.text)

        # 2.5 첫 번째 포스트의 작성자(author)가 포스트 영역에 있다(아직 구현할 수 없음)
        self.assertIn(self.user_obama.username.upper(), post_area.text)

        # 2.6 첫 번째 포스트의 내용(content)이 포스트 영역에 있다.
        self.assertIn(post_001.content, post_area.text)


































