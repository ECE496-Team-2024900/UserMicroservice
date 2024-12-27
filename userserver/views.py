from django.core.serializers import serialize
from django.db.models import Q
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

@api_view(['GET'])
def search_patients(request):
    try:
        search_query = request.GET.get('query', '').strip()

        if not search_query:
            return JsonResponse({"message": "No search query provided"}, status=400)

        # Split the search string into individual words
        search_terms = search_query.split()

        # Build the query dynamically
        query = Q()
        if len(search_terms) == 1:
            # Single word: search in both first_name and last_name
            query = Q(first_name__icontains=search_terms[0]) | Q(last_name__icontains=search_terms[0])
        else:
            # Multiple words: match the first and last names in order
            for term in search_terms:
                query &= (Q(first_name__icontains=term) | Q(last_name__icontains=term))

        # Filter patients based on the query
        patients = Patients.objects.filter(query)

        if patients.exists():
            return JsonResponse({"message": list(patients.values())}, status=200)
        else:
            return JsonResponse({"message": "No patients found matching the query"}, status=404)

    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)
    

@api_view(['PUT'])
def create_patient(request):
    try:
        body = json.loads(request.body)
        
        # Extract fields
        required_fields = ["first_name", "last_name", "date_of_birth", "medical_ref_number", "email", "phone_num"]
        missing_fields = [field for field in required_fields if field not in body]
        
        if missing_fields:
            return JsonResponse({"message": f"Missing required fields: {', '.join(missing_fields)}"}, status=400)

        # Check for duplicate medical_ref_number or email
        if Patients.objects.filter(medical_ref_number=body['medical_ref_number']).exists():
            return JsonResponse({"message": "A patient with this Medical Reference Number already exists. New record not created."}, status=400)
        if Patients.objects.filter(email=body['email']).exists():
            return JsonResponse({"message": "A patient with this email address already exists. New record not created."}, status=400)

        # Create and save the patient record
        new_patient = Patients(
            first_name=body['first_name'],
            last_name=body['last_name'],
            date_of_birth=body['date_of_birth'],
            medical_ref_number=body['medical_ref_number'],
            email=body['email'],
            phone_num=body['phone_num']
        )
        new_patient.save()

        return JsonResponse({"message": "Patient record created successfully"}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"message": "Invalid JSON body"}, status=400)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)