from urllib import unquote

from django.http import HttpResponse

from models import Article, UserProfile
from tasks import visit_article


def log_article(request):
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


def log_article_user(request, access_key):
    url = request.GET.get('url', False)
    try:
        profile = UserProfile.objects.get(access_key=access_key)
    except User.DoesNotExist:
        return HttpResponse('Invalid access key')
    
    if url:
        url = unquote(url)
        obj, created = Article.objects.get_or_create(url=url)
        
        if not obj in profile.articles.all():
            profile.articles.add(obj)
        
        visit_article.delay(obj.id)
        
        if created:
            return HttpResponse('Created new article: %s' % obj.url)
        else:
            return HttpResponse('Article already exists: %s' % obj.url)
    
    return HttpResponse('No URL specified')


def index(request):
    return request.Context({
        'articles': Article.objects.filter(visited__isnull=False).order_by('title')
    }).render_response('watcher/index.html')

