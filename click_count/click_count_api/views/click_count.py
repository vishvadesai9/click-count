from click_count_api.serializers import ClickCountSerializer
from django.db.models import Q, Sum
from rest_framework import views, status
from rest_framework.response import Response
from click_count_api.models import ClickCount
import json
import requests

class ClickModelView(views.APIView):

    # def list(self, request, *args, **kwargs):

    def post(self, request):
        ip_address = str(request.data["ip"]).strip()
        # ip_address = "155.98.131.1"
        request_url = 'https://geolocation-db.com/jsonp/' + ip_address
        response = requests.get(request_url)
        result = response.content.decode()
        result = result.split("(")[1].strip(")")
        location  = json.loads(result)

        queryset = ClickCount.objects.all()
        location_existing = queryset.filter(Q(country=location["country_name"]) & Q(city=location["city"]))
        
        if location_existing:
            count=location_existing.first().count+1
            location_existing.update(**{"count":count})
            location_existing.first().save()
            return Response(
            {"success": True, "message": "Click updated successfully"},
                status=status.HTTP_200_OK,
            )
        else:
            new_location = ClickCount.objects.create(country=location["country_name"],city=location["city"],count=1)
            return Response(
                {"success": True, "message": "Click recorded successfully"},
                status=status.HTTP_200_OK,
                )
    
    def get(self, request):
        queryset = ClickCount.objects.all().order_by('-count')
        total_count = ClickCount.objects.aggregate(Sum("count"))['count__sum'] 
        serializer_data = ClickCountSerializer(queryset,many=True)
        count_data = serializer_data.data
        return  Response(
                {"success": True, "total_count": total_count, "locations": count_data},
                status=status.HTTP_200_OK,
                )