from django.views.generic import ListView

from .models import Article


class ArticlesListView(ListView):
    template_name = 'blogapp/article_list.html'
    model = Article
    queryset = (Article.objects
                .defer('content')
                .select_related('author', 'category')
                .prefetch_related('tags')
                )
    context_object_name = 'articles'

