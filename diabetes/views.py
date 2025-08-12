from django.shortcuts import render
import os
import joblib
import numpy as np
from .models import DiabetesPrediction
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required 


# Create your views here.

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, 'diabetes', 'model_files', 'clinical_diabetes_model.pkl')

model = joblib.load(MODEL_PATH)

symptoms = [
    ('Polyuria', 'Excessive Urine'),
    ('Polydipsia', 'Excessive Thirst'),
    ('sudden_weight_loss', 'Sudden Weight Loss'),
    ('weakness', 'Weakness(tiredness)'),
    ('Polyphagia', 'Excessive Hunger'), 
    ('Genital_thrush', 'Genital Infection'),
    ('visual_blurring', 'Blurry Vision'),
    ('Itching', 'Itchy Skin'),
    ('Irritability', 'Irritability'),
    ('delayed_healing', 'Slow Wound Healing'),
    ('partial_paresis', 'Muscle Weakness'),
    ('muscle_stiffness', 'Muscle Stiffness'),
    ('Alopecia', 'Hair Loss'),
    ('Obesity', 'Obesity'),
]

# mapping the symptoms to their respective field names
field_names = {
    'Polyuria': 'Polyuria',
    'Polydipsia': 'Polydipsia',
    'sudden_weight_loss': 'sudden weight loss',
    'weakness': 'weakness',
    'Polyphagia': 'Polyphagia',
    'Genital_thrush': 'Genital thrush',
    'visual_blurring': 'visual blurring',
    'Itching': 'Itching',
    'Irritability': 'Irritability',
    'delayed_healing': 'delayed healing',
    'partial_paresis': 'partial paresis',
    'muscle_stiffness': 'muscle stiffness',
    'Alopecia': 'Alopecia',
    'Obesity': 'Obesity',
}

@login_required 
def home(request):
    # input from the user
    if request.method == 'POST':
        Age = int(request.POST.get('age'))
        gender = request.POST.get('Gender')

        Gender = 1 if gender == 'Male' else 0 # converting the gender to 0 and 1

        symptoms_value = []
        symptoms_dict = {}
        for field, _ in symptoms:
            value = 1 if request.POST.get(field) else 0
            symptoms_dict[field] = bool(value)

            model_field = field_names.get(field, field)
            symptoms_value.append(value)

        final_input = [Age, Gender] + symptoms_value

        prediction = model.predict([final_input])[0]
        result = "The patient <strong>has diabetes</strong>." if prediction == 1 else "The patient <strong>does not have diabetes</strong>."
        prediction_result = bool(prediction)


        # Save the prediction to the database
        DiabetesPrediction.objects.create(
            user=request.user, 
            Age=Age,
            Gender=Gender,
            symptoms=", ".join([label for field, label in symptoms if symptoms_dict[field]]),
            Polyuria=symptoms_dict['Polyuria'],
            Polydipsia=symptoms_dict['Polydipsia'],
            sudden_weight_loss=symptoms_dict['sudden_weight_loss'],
            weakness=symptoms_dict['weakness'],
            Polyphagia=symptoms_dict['Polyphagia'],
            Genital_thrush=symptoms_dict['Genital_thrush'],
            visual_blurring=symptoms_dict['visual_blurring'],
            Itching=symptoms_dict['Itching'],
            Irritability=symptoms_dict['Irritability'],
            delayed_healing=symptoms_dict['delayed_healing'],
            partial_paresis=symptoms_dict['partial_paresis'],
            muscle_stiffness=symptoms_dict['muscle_stiffness'],
            Alopecia=symptoms_dict['Alopecia'],
            Obesity=symptoms_dict['Obesity'],
            prediction=prediction_result
        )


        context = {
            'result': result,
            'age': Age,
            'gender': gender,
            'symptoms': symptoms,
            'selected_symptoms': [label for field, label in symptoms if symptoms_dict[field]],
        }

        return render(request, 'home.html', context)



    return render(request, 'home.html', {'symptoms': symptoms})
