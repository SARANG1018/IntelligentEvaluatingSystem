from django import forms
from django.contrib.auth.models import User
from . import models

class CourseForm(forms.ModelForm):
    class Meta:
        model=models.Course
        fields=['course_name','question_number','total_marks']

class QuestionForm(forms.ModelForm):
    
    courseID=forms.ModelChoiceField(queryset=models.Course.objects.all(),empty_label="Course Name", to_field_name="id")
    class Meta:
        model=models.Question
        fields=['marks','question','difficulty','option1','option2','option3','option4','answer']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3, 'cols': 50})
        }