from django.db import models

class Article(models.Model):
    url = models.CharField(max_length=255, db_index=True)
    title = models.CharField(max_length=255, blank=True)
    links = models.ManyToManyField('self', symmetrical=False)
    visited = models.BooleanField(default=False, db_index=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    
    def __unicode__(self):
        return self.title
