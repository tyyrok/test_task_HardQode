from django.shortcuts import render
from django.db.models import Prefetch, Q, Count, Sum
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserProducts, Lesson, UserLessonInfo, Product
from .serializers import UserProductSerializer
from django.contrib.auth import get_user_model
from datetime import timedelta
import re

User = get_user_model()

class StatisticsView(APIView):
    
    def get(self, request):
        result = []
        products_list = Product.objects.all().prefetch_related('userproducts_set').prefetch_related('lesson_set__userlessoninfo_set')
        if len(products_list) == 0:
            raise ValidationError(detail={"detail": "Products doesn't exist"})
        total_users = User.objects.all().count()
        
        for product in products_list:
            obj = {}
            obj['Product Id'] = product.pk
            obj['Product'] = product.title
            obj['Number of students'] = product.userproducts_set.all().count()

            count = 0
            for lesson in product.lesson_set.all():
                for userlesson in lesson.userlessoninfo_set.all():
                    if userlesson.status == 'Watched':
                        count += 1
            obj['Number of watched lessons'] = count
            
            # Below is a version with cool stuff that takes more requests to Db
            """
            obj['Number of watched lessons'] = (
                product.lesson_set.all().aggregate(num=Count("userlessoninfo", 
                                                    filter=Q(userlessoninfo__status="Watched")))
            )['num']
            """
            time_spent = timedelta()
            for lesson in product.lesson_set.all():
                for userlesson in lesson.userlessoninfo_set.all():
                    time_spent += userlesson.watched_time
            obj['Students time spent in sec'] = time_spent 
            
            # Below is a version with cool stuff that takes more requests to Db
            """
            obj['Students time spent in sec'] = (
                product.lesson_set.all().aggregate(num=Sum("userlessoninfo__watched_time"))
            )['num']
            """

            obj['Percent of purchasing'] = ( 
                f"{product.userproducts_set.all().count() / total_users :.2%}"
            )
            
            result.append(obj)
        
        return Response(data=result, status=status.HTTP_200_OK)

class UserProductView(ListAPIView):
    queryset = UserProducts.objects.none()
    serializer_class = UserProductSerializer
    
    def get_queryset(self):
        user_id = self.kwargs['user_id']

        userlesson = UserLessonInfo.objects.filter(user__id=user_id)
        queryset = (
            UserProducts.objects.filter(user__id=user_id) #filter(product__lesson__userlessoninfo__user=user)
                                .prefetch_related(Prefetch('product__lesson_set__userlessoninfo_set',
                                                    queryset=userlesson))
            )
        
        return queryset
    
class UserProductDetailView(RetrieveAPIView):
    queryset = UserProducts.objects.none()
    serializer_class = UserProductSerializer
    
    def get_object(self):
        user_id = self.kwargs['user_id']
        product_id = self.kwargs['product_id']
        userlesson = UserLessonInfo.objects.filter(user__id=user_id)
        obj = ( 
                   UserProducts.objects.filter(user__id=user_id, product__id=product_id)
                                        .prefetch_related(Prefetch('product__lesson_set__userlessoninfo_set',
                                                    queryset=userlesson))
            )
        if len(obj) == 0:
            raise ValidationError(detail={'detail': 'Incorrect product id'})
        return obj[0]
        
    

    