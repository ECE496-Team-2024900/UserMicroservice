from django.core.serializers import serialize
from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import Patients, Clinicians
import json

def index(request):
    return JsonResponse({"message": "This is the user microservice"})

@api_view(['GET'])
def find_all_patients(request):
    try:
        obj = Patients.objects.all()
        if (obj is not None):
            return JsonResponse({"message": list(obj.values())}, status=200)
        else:
            return JsonResponse({"message": "No patients exist"}, status=404)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)

@api_view(['GET'])
def get_clinician_info(request):
    params = request.query_params
    try:
        obj = Clinicians.objects.filter(email=params['email']).first()
        if (obj is not None):
            return JsonResponse({"message": model_to_dict(obj)}, status=200)
        else:
            return JsonResponse({"message": "Clinician with that email does not exist"}, status=404)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)
    
@api_view(['GET'])
def get_patient_info(request):
    params = request.query_params
    try:
        obj = Patients.objects.filter(email=params['email']).first()
        if (obj is not None):
            return JsonResponse({"message": model_to_dict(obj)}, status=200)
        else:
            return JsonResponse({"message": "Patient with that email does not exist"}, status=404)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)

@api_view(['PUT'])
# Adding a new clinician
def add_clinician(request):
    try:
        # Adding a clinician object based on provided body
        new_clincian = json.loads(request.body)
        Clinicians.objects.create(**new_clincian)
    except Exception as e:
        return JsonResponse({'message':str(e)}, status=500)
    return JsonResponse({'message':'Clinician was successfully added'}, status=200)

@api_view(['GET'])
# Checking if clinician exists in DB (i.e. if they are registered)
def check_if_clinician_exists(request):
    try:
        # Checking if a clinician with given email exists
        # Email is the primary key, hence defines whether clinician exists
        email = request.query_params['email']
        clinician = Clinicians.objects.filter(email=email).first()
        if (clinician is not None):
            return JsonResponse({"message": "Clinician registered"}, status=200)
        else:
            return JsonResponse({"message": "Clinician not registered"}, status=201)
    except Exception as e:
        return JsonResponse({'message':str(e)}, status=500)
    