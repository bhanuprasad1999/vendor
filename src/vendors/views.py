from rest_framework.decorators import api_view
from django.http import JsonResponse
from vendors.models import VendorModel
from vendors.serializers import VendorSerializer
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

id = openapi.Parameter(
    'id', openapi.IN_QUERY, description="pass id's", type=openapi.TYPE_STRING)
search = openapi.Parameter('name', openapi.IN_QUERY, description="search query", type=openapi.TYPE_STRING)

# Returns the single vendor details which can viewed, updated, deleted..
@swagger_auto_schema(method='PUT',request_body=VendorSerializer ,manual_parameters=[id])
@swagger_auto_schema(method='DELETE', manual_parameters=[id])
@swagger_auto_schema(method='GET', manual_parameters=[id])
@api_view(['GET', 'PUT', 'DELETE'])
def vendor(request):
    try:
        object = VendorModel.objects.get(id=int(request.GET['id']))
        print(object)
        if request.method == 'GET':
            serializer = VendorSerializer(object)
            return JsonResponse({'data': serializer.data})
        elif request.method == 'PUT':
            serializer = VendorSerializer(object, data=request.data)
            if serializer.is_valid():
                serializer.save()
            return JsonResponse({'data': serializer.data})
        elif request.method == 'DELETE':
            object.delete()
            return JsonResponse({'message':'successfully deleted'})
    except Exception as e:
        return JsonResponse({'error': f'warning :{e}!'})


# new object is created and return values of the object

@swagger_auto_schema(method='post', request_body=VendorSerializer)
@api_view(['POST'])
def create_vendor(request):
    if not VendorModel.objects.filter(name=request.data['name']).exists():

        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'data': serializer.data})
    else:
        return JsonResponse({'error': 'warning: Vendor is already exists!'})


# Getting the list of vendors in the database..


@api_view(['GET'])
def list_vendors(request):
    objects = VendorModel.objects.all()
    serializer = VendorSerializer(objects, many=True)
    return JsonResponse({'data': serializer.data})


# returning the search results based on the name, location, rating

@swagger_auto_schema(method='GET',request_body=VendorSerializer ,manual_parameters=[search])
@api_view(['GET'])
def vendor_search(request):
    search = request.GET
    if search != {}:
        objects = VendorModel.objects.filter(Q(name__contains=search.get('name', 0)) | Q(
            location__contains=search.get('location', 0)) | Q(rating__contains=search.get('rating', -1)))
        if not objects.exists():
            return JsonResponse({'error': f'No Vendor existed!'})
        serializer = VendorSerializer(objects, many=True)
        return JsonResponse({'data': serializer.data})
    else:
        return JsonResponse({'error': 'provide a valid search query'})
