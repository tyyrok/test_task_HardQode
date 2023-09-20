from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()

class Product(models.Model):
    title = models.CharField(max_length=128)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f"{self.title} by {self.owner}"
    
class UserProducts(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f"pk-{self.pk}, User-{self.user.username}"

class Lesson(models.Model):
    product = models.ManyToManyField(to=Product, blank=True)
    title = models.CharField(max_length=128)
    video_link = models.URLField()
    duration = models.DurationField()
    
    def __str__(self) -> str:
        return f"{self.title} - {self.video_link} - {self.duration}"

class UserLessonInfo(models.Model):
    STATUS = [
        ('YES', 'Watched'),
        ('NO', 'Not watched'),
    ]
    watched_time = models.DurationField(default=0)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(to=Lesson, on_delete=models.CASCADE)
    
    @property
    def status(self):
        if self.watched_time >= self.lesson.duration * 0.8:
            return self.STATUS[0][1]
        else:
            return self.STATUS[1][1]
        
    def __str__(self) -> str:
        return f"Lesson - {self.lesson.title}, User - {self.user.username}, Status - {self.status}"
        