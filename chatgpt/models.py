from django.db import models

class ChatHistory(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    query = models.TextField()
    answer = models.TextField()
    
# Vector DB
class Vector(models.Model):
    content = models.TextField()
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.content[:50]