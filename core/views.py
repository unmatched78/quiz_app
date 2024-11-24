import random  
from django.db.models import Count  
from rest_framework import viewsets, status  
from rest_framework.response import Response  
from rest_framework.permissions import IsAuthenticated  
from django.contrib.auth.models import User  
from rest_framework.authtoken.models import Token  
from django.contrib.auth import authenticate  
from .models import Aquiz, Zanswer, CorrectQuestion  
from .serializers import QuizSerializer, CorrectQuestionSerializer  

class QuizViewSet(viewsets.ViewSet):  
    permission_classes = [IsAuthenticated]  # Protect this view  

    def list(self, request):  
        # Get questions that the user has not answered correctly  
        answered_questions = CorrectQuestion.objects.filter(user=request.user).values_list('question', flat=True)  
        questions = Aquiz.objects.exclude(id__in=answered_questions)  

        if not questions.exists():  
            return Response({'error': 'No more questions available'}, status=status.HTTP_404_NOT_FOUND)  # we can change it later , to tell the user that s/he have successed everything.

        random_questions = random.sample(list(questions), min(1, questions.count()))  
        serializer = QuizSerializer(random_questions, many=True)  
        return Response(serializer.data)  

    def create(self, request):  
        user = request.user  
        answered_questions = CorrectQuestion.objects.filter(user=user).values_list('question', flat=True)  
        response_data = []  # To store the results for each question  

        for answer in request.data.get('answers', []):  
            question_id = answer.get('question_id')  

            # Validation: check if the user has already answered this question correctly  
            if question_id in answered_questions:  
                return Response({'error': f'You have already answered question {question_id} correctly.'},   
                                status=status.HTTP_400_BAD_REQUEST)  

            selected_answer_id = answer.get('selected_answer_id')  
            correct_answer = Zanswer.objects.filter(question_id=question_id, is_correct=True).first()  

            if not correct_answer:  
                return Response({'error': f'No correct answer found for question {question_id}'},   
                                status=status.HTTP_400_BAD_REQUEST)  

            # Determine if the selected answer is correct  
            is_correct = correct_answer.id == selected_answer_id  
            response_data.append({  
                'question_id': question_id,  
                'selected_answer_id': selected_answer_id,  
                'correct_answer_id': correct_answer.id,  
                'is_correct': is_correct  
            })  

            # Save correct answer if the user answered correctly  
            if is_correct:  
                CorrectQuestion.objects.get_or_create(question_id=question_id, user=user)  

        return Response({  
            'status': 'Answers submitted',  
            'results': response_data  
        }, status=status.HTTP_201_CREATED)  
class UserViewSet(viewsets.ViewSet):  
    def create(self, request):  
        # User registration  
        username = request.data.get('username')  
        password = request.data.get('password')  
        user = User.objects.create_user(username=username, password=password)  
        token = Token.objects.create(user=user)  
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)  

    def login(self, request):  
        # User login  
        username = request.data.get('username')  
        password = request.data.get('password')  
        user = authenticate(username=username, password=password)  
        if user is not None:  
            token, _ = Token.objects.get_or_create(user=user)  
            return Response({'token': token.key}, status=status.HTTP_200_OK)  
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)  

    def logout(self, request):  
        # User logout  
        token = request.data.get('token')  # Accepting token from the request body  , bcz, using the header is not possible using DRF testing

        if not token:  
            return Response({'error': 'No token provided'}, status=status.HTTP_400_BAD_REQUEST)  

        try:  
            token_obj = Token.objects.get(key=token)  
            token_obj.delete()  # Delete the token to log the user out  
            return Response({'status': 'Logged out'}, status=status.HTTP_200_OK)  
        except Token.DoesNotExist:  
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)  
#         def logout(self, request):  
#         # User logout  
#         request.user.auth_token.delete()  # great for submitting the user token using header
#         return Response({'status': 'Logged out'}, status=status.HTTP_200_OK)