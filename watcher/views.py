from urllib import unquote
from django.http import HttpResponse
from models import Article


def add_link(request):
    url = request.GET.get('url', False)
    
    if url:
        url = unquote(url)
        article, created = Article.objects.get_or_create(url=url)
        article.visit()
        
        if created:
            return HttpResponse('Created new article: %s' % url)
    
    return HttpResponse('')

