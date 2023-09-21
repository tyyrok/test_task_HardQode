from django.shortcuts import render
from django.db.models import Prefetch
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.exceptions import ValidationError
from .models import UserProducts, Lesson, UserLessonInfo
from .serializers import UserProductSerializer
from django.contrib.auth import get_user_model
import re

User = get_user_model()

class UserProductView(ListAPIView):
    queryset = UserProducts.objects.none()
    serializer_class = UserProductSerializer
    
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise ValidationError(detail={'detail': 'Incorrect user id'})
        try:
            userlesson = UserLessonInfo.objects.filter(user=user)
            queryset = (
                UserProducts.objects.filter(user=user) #filter(product__lesson__userlessoninfo__user=user)
                                  .prefetch_related(Prefetch('product__lesson_set__userlessoninfo_set',
                                                    queryset=userlesson))
            )
        except UserProducts.DoesNotExist:
            raise ValidationError(detail={'detail': 'Incorrect user id'})
        
        return queryset
    
class UserProductDetailView(RetrieveAPIView):
    queryset = UserProducts.objects.none()
    serializer_class = UserProductSerializer
    
    def get_object(self):
        user_id = self.kwargs['user_id']
        product_id = self.kwargs['product_id']
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise ValidationError(detail={'detail': 'Incorrect user id'})
        userlesson = UserLessonInfo.objects.filter(user=user)
        obj = ( 
                   UserProducts.objects.filter(user__id=user_id, product__id=product_id)
                                        .prefetch_related(Prefetch('product__lesson_set__userlessoninfo_set',
                                                    queryset=userlesson))
            )
        if len(obj) == 0:
            raise ValidationError(detail={'detail': 'Incorrect product id'})
        return obj[0]
        
    

    