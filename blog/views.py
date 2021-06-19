from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Category


class PostList(ListView):
    model = Post
    ordering = '-pk'

    def get_context_data(self,  **kwargs):
        contxet = super(PostList, self).get_context_data()
        contxet['categories'] = Category.objects.all()
        contxet['no_category_post_count'] = Post.objects.filter(category=None).count()
        return contxet


class PostDetail(DetailView):
    model = Post

    def get_context_data(self,  **kwargs):
        contxet = super(PostDetail, self).get_context_data()
        contxet['categories'] = Category.objects.all()
        contxet['no_category_post_count'] = Post.objects.filter(category=None).count()
        return contxet


def category_page(request, slug):
    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,
            'categories': Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category=None).count(),
            'category': category,
        }
    )