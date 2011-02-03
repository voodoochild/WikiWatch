from urllib import unquote

from django.http import HttpResponse

from models import Article
from tasks import visit_article


def add_link(request):
    url = request.GET.get('url', False)
    
    if url:
        url = unquote(url)
        obj, created = Article.objects.get_or_create(url=url)
        visit_article.delay(obj.id)
        
        if created:
            return HttpResponse('Created new article: %s' % obj.url)
        else:
            return HttpResponse('Article already exists: %s' % obj.url)
    
    return HttpResponse('No URL specified')


def index(request):
    return request.Context({
        'articles': Article.objects.filter(visited=True).order_by('title')
    }).render_response('watcher/index.html')

