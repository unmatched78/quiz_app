# # urls.py  
# from django.urls import path, include  
# from rest_framework.routers import DefaultRouter  
# from .views import QuizViewSet, UserViewSet  

# router = DefaultRouter()  
# router.register(r'quizzes', QuizViewSet, basename='quiz')  
# router.register(r'users', UserViewSet, basename='user')  

# urlpatterns = [  
#     path('', include(router.urls)),  
# ]

# core/urls.py  
from django.urls import path, include  
from rest_framework.routers import DefaultRouter  
from .views import QuizViewSet, UserViewSet  

router = DefaultRouter()  
router.register(r'quizzes', QuizViewSet, basename='quiz')  
router.register(r'users', UserViewSet, basename='user')  

urlpatterns = [  
    path('', include(router.urls)),  
    path('users/login/', UserViewSet.as_view({'post': 'login'}), name='user-login'),  # Login URL  
    path('users/logout/', UserViewSet.as_view({'post': 'logout'}), name='user-logout'),  # Logout URL  
    # Other URL patterns can go here...  
]