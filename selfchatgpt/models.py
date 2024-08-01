from django.db import models

class ChatHistory(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    query = models.TextField()
    answer = models.TextField()