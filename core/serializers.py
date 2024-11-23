# serializers.py  
from rest_framework import serializers  
from .models import Aquiz, Zanswer, CorrectQuestion  

class AnswerSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = Zanswer  
        fields = ['id', 'answer_text', 'is_correct', 'answer_image']  

class QuizSerializer(serializers.ModelSerializer):  
    answers = AnswerSerializer(many=True, read_only=True)  

    class Meta:  
        model = Aquiz  
        fields = ['id', 'question', 'question_image', 'answers']  

class CorrectQuestionSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = CorrectQuestion  
        fields = ['question', 'user', 'created_at']