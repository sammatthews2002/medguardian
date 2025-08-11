from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class DiabetesPrediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    Age = models.IntegerField()
    Gender = models.CharField(max_length = 10)
    symptoms = models.TextField()
    Polyuria = models.BooleanField(default=False)
    Polydipsia = models.BooleanField(default=False)
    sudden_weight_loss = models.BooleanField(default=False)
    weakness = models.BooleanField(default=False)
    Polyphagia = models.BooleanField(default=False) 
    Genital_thrush = models.BooleanField(default=False)
    visual_blurring = models.BooleanField(default=False)
    Itching = models.BooleanField(default=False)
    Irritability = models.BooleanField(default=False)
    delayed_healing = models.BooleanField(default=False)
    partial_paresis = models.BooleanField(default=False)
    muscle_stiffness = models.BooleanField(default=False)
    Alopecia = models.BooleanField(default=False)
    Obesity = models.BooleanField(default=False)    
    prediction = models.BooleanField(default=False)
    
    