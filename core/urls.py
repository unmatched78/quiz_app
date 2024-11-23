# urls.py  
from django.urls import path, include  
from rest_framework.routers import DefaultRouter  
from .views import QuizViewSet, UserViewSet  

router = DefaultRouter()  
router.register(r'quizzes', QuizViewSet, basename='quiz')  
router.register(r'users', UserViewSet, basename='user')  

urlpatterns = [  
    path('', include(router.urls)),  
]