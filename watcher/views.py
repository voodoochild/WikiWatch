import re
from urllib import unquote

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from models import Article, Category, Visit, UserProfile
from tasks import visit_article


def log_article_user(request, access_key):
    """
    Logs an article against the user identified using the unique
    access key.
    """
    url = request.GET.get('url', False)
    try:
        profile = UserProfile.objects.get(access_key=access_key)
    except UserProfile.DoesNotExist:
        return HttpResponse('Invalid access key')
    
    if url:
        url = unquote(url)
        
        # Don't ever add /wiki/Main_Page
        if re.match('^.+/wiki/Main_Page.*$', url):
            return HttpResponse('%s logged. Ignored.' % obj.url)
        
        # If this is a category page, create a Category object for it
        # and return a response without visiting it.
        if re.match('^.+/wiki/Category:.+$', url):
            obj, created = Category.objects.get_or_create(url=url)
            if created:
                return HttpResponse('%s logged. New category.' % obj.url)
            else:
                return HttpResponse('%s logged. Existing category.' % obj.url)
        
        # Not a category, so create and visit the article        
        obj, created = Article.objects.get_or_create(url=url)
        
        if not obj in profile.articles.all():
            profile.articles.add(obj)
        
        visit = Visit(
            user = profile.user,
            article = obj
        ).save()
        
        visit_article.delay(obj.id)
        
        if created:
            return HttpResponse('%s logged. New article.' % obj.url)
        else:
            return HttpResponse('%s logged. Existing article.' % obj.url)
    
    return HttpResponse('No URL specified')


def index(request):
    """
    Shows all logged articles.
    """
    return request.Context({
        'articles': Article.objects.filter(visited__isnull=False).order_by('title')
    }).render_response('watcher/index.html')


def user_index(request, username):
    """
    Shows logged articles for the specified user.
    """
    user = get_object_or_404(User, username=username)
    profile = user.get_profile()
    
    return request.Context({
        'user': user,
        'articles': profile.articles.filter(visited__isnull=False).order_by('title')
    }).render_response('watcher/user_index.html')


def user_logged_in_redirect(request):
    """
    If the current user is logged in, redirect them to their account page.
    """
    if request.user.is_authenticated():
        kwargs = {'username': request.user.username}
        return HttpResponseRedirect(reverse('watcher_user_index', kwargs=kwargs))
    else:
        return HttpResponseRedirect(reverse('watcher_index'))

