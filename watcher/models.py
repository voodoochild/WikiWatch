from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Category(models.Model):
    url = models.CharField(max_length=255, db_index=True)
    title = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    
    def __unicode__(self):
        return self.title


class Article(models.Model):
    url = models.CharField(max_length=255, db_index=True)
    title = models.CharField(max_length=255, blank=True)
    links = models.ManyToManyField('self', symmetrical=False)
    visited = models.DateTimeField(blank=True, null=True, db_index=True)
    categories = models.ManyToManyField(Category)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    
    def __unicode__(self):
        return self.title
    
    def user_visited_links(self, user):
        visited = 0
        profile = user.get_profile()
        
        for link in self.links.all():
            if link in profile.articles.all():
                visited = visited + 1
        
        return visited


class Visit(models.Model):
    user = models.ForeignKey(User)
    article = models.ForeignKey(Article)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    
    def __unicode__(self):
        return '%s: %s' % (self.user.username, self.article.title)


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    access_key = models.CharField(max_length=32, unique=True, db_index=True)
    articles = models.ManyToManyField(Article)
    
    def __unicode__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        if not self.access_key:
            from hashlib import md5
            from time import time
            m = md5()
            m.update(str(self.id))
            m.update(str(self.user.id))
            m.update(str(time()))
            key = m.hexdigest()
            
            while True:
                try:
                    # If the key is already in use, feed it back in
                    # and regenerate the hexdigest
                    UserProfile.objects.get(access_key=key)
                    m.update(key)
                    key = m.hexdigest()
                except UserProfile.DoesNotExist:
                    self.access_key = key
                    break
            
        return super(UserProfile, self).save(*args, **kwargs)
    
    def visited_articles(self):
        return Visit.objects.filter(user=self.user).order_by('created')

def auto_create_profile(sender, instance, created, **kwargs):
    if created:
        obj, created = UserProfile.objects.get_or_create(user=instance)
post_save.connect(auto_create_profile, sender=User)

