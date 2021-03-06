import re
import socket
import urllib2
from datetime import datetime
from celery.task import task
from BeautifulSoup import BeautifulSoup

from watcher.models import Article, Category

SOCKET_TIMEOUT = 10

@task
def visit_article(article_id):
    logger = visit_article.get_logger()
    
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        logger.info('Could not find an Article with id %d' % article_id)
        return False
    
    try:
        socket.setdefaulttimeout(SOCKET_TIMEOUT)
        request = urllib2.Request(article.url)
        request.add_header('User-Agent', 'Mozilla/5.0 (X11; U; Linux i686; \
            en-US) AppleWebKit/534.16 (KHTML, like Gecko) \
            Chrome/10.0.648.6 Safari/534.16')
        html = urllib2.urlopen(request).read()
    except urllib2.HTTPError, err:
        logger.error(err)
        return False
    except urllib2.URLError, err:
        logger.error(err)
        return False
    
    try:
        soup = BeautifulSoup(unicode(html, 'utf-8'))
    except UnicodeDecodeError, err:
        logger.error(err)
        return False
    
    # Set a title for this article if there isn't one
    if not article.title:
        try:
            h1 = soup('h1')
            h1 = h1[0]
            article.title = h1.find('i').string if h1.find('i') else h1.string
        except AttributeError, err:
            logger.info(err)
    
    # Loop through all links in the article
    for tag in soup('a'):
        try:
            href = tag['href']
            title = tag['title']
            
            if re.match('^/wiki/.+$', href):
                # Ignore if it is /wiki/Main_Page
                if re.match('^/wiki/Main_Page.*$', href):
                    continue;
                
                # Remove any anchor from the end of the url
                regex = re.compile('^(/wiki/.+)#.*$')
                r = regex.search(href)
                try:
                    href = r.groups()[0]
                except AttributeError:
                    pass
                
                # Check to see if any banned namespaces are present
                pattern = ''.join(['^/wiki/(Wikipedia|Special|Help|Talk|File|',
                    'Portal|Template|Template_talk):.+$'])
                
                if not re.match(pattern, href):
                    # Category
                    if re.match('^/wiki/Category:.+$', href):
                        logger.info('Found category %s (%s)' % (href, title))
                        url = 'http://en.wikipedia.org%s' % href
                        obj, created = Category.objects.get_or_create(url=url)
                        if title:
                            obj.title = title.replace('Category:', '')
                            obj.save()
                        if created:
                            logger.info('Created new category: %s' % obj.url)
                        if not obj in article.categories.all():
                            article.categories.add(obj)
                    
                    # Article
                    else:
                        logger.info('Found article %s (%s)' % (href, title))
                        url = 'http://en.wikipedia.org%s' % href
                        obj, created = Article.objects.get_or_create(url=url)
                        if title:
                            obj.title = title
                            obj.save()
                        if created:
                            logger.info('Created new article: %s' % obj.url)
                        if not obj == article:
                            article.links.add(obj)
        except KeyError:
            pass
    
    article.visited = datetime.now()
    article.save()
    
    return True

