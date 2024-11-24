from django.core.serializers import serialize
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import Patients
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