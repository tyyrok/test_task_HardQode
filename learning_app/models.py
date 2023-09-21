from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Product(models.Model):
    title = models.CharField(max_length=128)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f"{self.title}"
    
class UserProducts(models.Model):
    class Meta:
        unique_together = ['user', 'product']
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, null=True)
    
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
    class Meta:
        unique_together = ['user', 'lesson']
        
    STATUS = [
        ('YES', 'Watched'),
        ('NO', 'Not watched'),
    ]
    watched_time = models.DurationField(default=0)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(to=Lesson, on_delete=models.CASCADE)
    last_time_watched = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUS, max_length=12, blank=True)
        
    def __str__(self) -> str:
        return f"pk-{self.pk}"
    
    def save(self, *args, **kwargs) -> None:
        if self.watched_time >= self.lesson.duration * 0.8:
            self.status = self.STATUS[0][1]
        else:
            self.status = self.STATUS[1][1]
        print(self.status)
        return super().save(*args, **kwargs)
        