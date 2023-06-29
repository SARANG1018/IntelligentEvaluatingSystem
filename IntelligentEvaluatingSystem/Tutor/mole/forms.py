from django.forms import ModelForm
from .models import *

class addQuestionform(ModelForm):
    class Meta:
        model=Question
        fields="__all__"