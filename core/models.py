from django.db import models  
from django.contrib.auth.models import User  

class Aquiz(models.Model):  
    question = models.CharField(max_length=10000, null=True, blank=True)  
    question_image = models.ImageField(upload_to="images", null=True, blank=True)  

    def __str__(self):  
        return self.question  

class Zanswer(models.Model):  
    question = models.ForeignKey(Aquiz, related_name='answers', on_delete=models.CASCADE)  
    answer_text = models.CharField(max_length=500, null=True, blank=True)  
    is_correct = models.BooleanField(default=False)  # Default to False to avoid incorrect assumptions  
    answer_image = models.ImageField(upload_to="images", null=True, blank=True)  

    def __str__(self):  
        return f"{self.answer_text} (Correct: {self.is_correct})"  

class CorrectQuestion(models.Model):  
    question = models.ForeignKey(Aquiz, on_delete=models.CASCADE)  
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    created_at = models.DateTimeField(auto_now_add=True)  

    class Meta:  
        unique_together = ('question', 'user')  

    def __str__(self):  
        return f"{self.user.username} answered {self.question.question} well"