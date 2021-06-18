from django.test import TestCase, Client
from django.contrib.auth.models import User
from bs4 import BeautifulSoup
from .models import Post


class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_obama = User.objects.create_user(username='obama', password='somepassword')
        self.user_trump = User.objects.create_user(username='trump', password='somepassword')

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

    def test_post_list(self):
        # 1.1 포스트 목록 페이지를 가져온다.
        response = self.client.get('/blog/')
        # 1.2 장상적으로 페이지가 로드된다.
        self.assertEqual(response.status_code, 200)
        # 1.3 페이지 타이틀은 'Blog'이다.
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text, 'Blog')
        # 1.4 내비게이션 바가 있고 Blog, About Me라는 문구가 내비게이션 바에 있다.
        self.navbar_tast(soup)

        # 2.1 메인 영역에 게시물(포스트)이 하나도 없다면
        self.assertEqual(Post.objects.count(), 0)
        # 2.2 '아직 게시물이 없습니다'라는 문구가 보인다.
        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다', main_area.text)

        # 3.1 게시물이 2개 있다면
        post_001 = Post.objects.create(
            title='첫번째 포스트입니다',
            content='헬로 윌드, 위아더월드',
            author=self.user_obama
        )
        post_002 = Post.objects.create(
            title='두번째 포스트입니다',
            content='1등이 전부는 아니잖아요?',
            author=self.user_trump
        )
        self.assertEqual(Post.objects.count(), 2)

        # 3.2 포스트 목록 페이지를 새로고침했을 때
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(response.status_code, 200)
        # 3.3 메인 영역에 포스트 2개의 타이틀이 존재한다.
        main_area = soup.find('div', id='main-area')
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)
        # 3.4 '아직 게시물이 없습니다'라는 문구는 더 이상 보이지 않는다.
        self.assertNotIn('아직 게시물이 없습니다', main_area.text)
        # 3.4 작성자(author)가 메인 영역에 존재한다.
        self.assertIn(self.user_obama.username.upper(), main_area.text)
        self.assertIn(self.user_trump.username.upper(), main_area.text)

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


































