import re
import urllib2
from BeautifulSoup import BeautifulSoup
from django.db import models

class Article(models.Model):
    url = models.CharField(max_length=255, db_index=True)
    title = models.CharField(max_length=255, blank=True)
    links = models.ManyToManyField('self', symmetrical=False)
    visited = models.BooleanField(default=False, db_index=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    
    def __unicode__(self):
        return self.title
    
    def visit(self):
        # If the url 404s, the object should probably be flagged or removed
        try:
            request = urllib2.Request(self.url)
            request.add_header('User-Agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US) \
                AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.6 Safari/534.16')
            html = urllib2.urlopen(request).read()
        except urllib2.HTTPError, error:
            print error
            return
        except urllib2.URLError, error:
            print error
            return
        
        try:
            soup = BeautifulSoup(unicode(html, 'utf-8'))
        except UnicodeDecodeError:
            return
        
        tags = soup('a')
        links = []
        
        for tag in tags:
            try:
                href = tag['href']
                
                # Should this exclude /wiki/Wikipedia: and /wiki/Special:
                if re.match('^/wiki/.+$', href):
                    print href
            except KeyError:
                pass
        
        # get_or_create an object for each linked article
        
        # add linked article objects to article.links
        
        # self.visited = True
        
        return self.save()

