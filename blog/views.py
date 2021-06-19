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
