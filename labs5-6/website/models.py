from django.db import models

class Record(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    keyword = models.CharField(max_length=255)
    publication = models.CharField(max_length=255)
    resource = models.CharField(max_length=255)
    content = models.TextField()
    date_published = models.DateField()

    def __str__(self):
        return f"{self.title} - {self.keyword}"
class Keyword(models.Model):
    word = models.CharField(max_length=100, unique=True)
    frequency = models.IntegerField(default=0)
    def __str__(self):
        return self.word

