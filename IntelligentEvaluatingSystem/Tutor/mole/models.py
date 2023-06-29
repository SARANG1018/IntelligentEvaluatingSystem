from django.db import models
import uuid

# Create your models here.
class BaseModel(models.Model):
    uid=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now_add=True)

    class Meta:
        abstract = True

class Category(BaseModel):
    category_name=models.CharField(max_length=100)

    def __str__(self):
        return self.category_name
    
class Question(BaseModel): 
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    question = models.CharField(max_length=200,null=True)
    op1 = models.CharField(max_length=200,null=True)
    op2 = models.CharField(max_length=200,null=True)
    op3 = models.CharField(max_length=200,null=True)
    op4 = models.CharField(max_length=200,null=True)
    ans = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.question



