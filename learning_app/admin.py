from django.contrib import admin
from .models import UserProducts, Product, UserLessonInfo, Lesson

# Register your models here.
admin.site.register(UserLessonInfo)
admin.site.register(Product)
admin.site.register(Lesson)
admin.site.register(UserProducts)