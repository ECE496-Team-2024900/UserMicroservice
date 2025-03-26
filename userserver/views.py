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
        # Filter patient records using the email parameter that was passed in
        obj = Patients.objects.filter(medical_ref_number=params['id']).first()
        if (obj is not None):
            # Patient with that email found - use model_to_dict to return a dictionary so that attributes can be accessed by name
            return JsonResponse({"message": model_to_dict(obj)}, status=200)
        else:
            # Patient with that email not found
            return JsonResponse({"message": "Patient with that email does not exist"}, status=404)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)
    
# Retrieves the patient record that has the specified email address
# Expects an email to be passed in
# Returns a dictionary object containing all fields of the patient record
@api_view(['GET'])
def get_patient_info_by_email(request):
    params = request.query_params
    try:
        # Filter patient records using the email parameter that was passed in 
        obj = Patients.objects.filter(email=params['email']).first()
        if (obj is not None):
            # Patient with that email found - use model_to_dict to return a dictionary so that attributes can be accessed by name
            return JsonResponse({"message": model_to_dict(obj)}, status=200)
        else:
            # Patient with that email not found
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
    
# Performs a search of patient records by first and last name
# Expects a search string (containing patient name) that is to be used for the filtering
# Returns a list of all patients whose first and/or last name matches the search query
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
    
# Creates a new patient record in database
# Expects a JSON body with key-value pairs that denote the fields and their values
# Fields/keys required in JSON: first_name, last_name, date_of_birth, medical_ref_number, email, phone_num
# Returns a success or error message
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
