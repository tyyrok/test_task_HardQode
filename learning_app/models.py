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
    
    
    @property
    def status(self):
        if self.watched_time >= self.lesson.duration * 0.8:
            return self.STATUS[0][1]
        else:
            return self.STATUS[1][1]
        
    def __str__(self) -> str:
        return f"pk-{self.pk}"
    
    def save(self, *args, **kwargs) -> None:
        """Overriding save method to prevent User add info about 
        unvailable lessons in admin panel
        """
        available_products = self.lesson.product.all()
        available_lessons = self.user.userproducts.product.all()
        for lesson in available_lessons:
            print(lesson)
            if lesson in available_products:
                return super().save(*args, **kwargs)
        return 
        