from click_count_api.serializers import ClickCountSerializer
from django.db.models import Q, Sum, F
from rest_framework import views, status
from rest_framework.response import Response
from click_count_api.models import ClickCount
import json
import requests
from django.http import JsonResponse

class ClickModelView(views.APIView):

    # def list(self, request, *args, **kwargs):

    def post(self, request):
        ip_address = request.data.get("ip","").strip()
        if not ip_address:
            obj, created = ClickCount.objects.get_or_create(country="Anonymous", city="Anonymous",
                                                        defaults={"count": 0})
            obj.count = F("count") + 1
            obj.save()
        else:
            request_url = f'https://geolocation-db.com/jsonp/{ip_address}'
            response = requests.get(request_url)
            result = response.content.decode()
            result = result.split("(")[1].strip(")")
            location  = json.loads(result)
            print(location)
            if not location['city'] or not location['country_name']:
                obj, created = ClickCount.objects.get_or_create(country="Anonymous", city="Anonymous",
                                                            defaults={"count": 0})
                obj.count = F("count") + 1
                obj.save()
            else:
                obj, created = ClickCount.objects.get_or_create(country=location["country_name"], city=location["city"],
                                                                defaults={"count": 0})
                obj.count = F("count") + 1
                obj.save()

        message = "Click updated successfully" if not created else "Click recorded successfully"
        return JsonResponse({"success": True, "message": message}, status=200)
        
    
    def get(self, request):
        queryset = ClickCount.objects.all()
        if queryset:
            queryset = queryset.order_by('-count')
            total_count = ClickCount.objects.aggregate(Sum("count"))['count__sum'] 
            serializer_data = ClickCountSerializer(queryset,many=True)
            count_data = serializer_data.data
            return  Response(
                    {"success": True, "total_count": total_count, "locations": count_data},
                    status=status.HTTP_200_OK,
                    )
        else:
             return  Response(
                    {"success": True, "total_count": 0, "locations": []},
                    status=status.HTTP_200_OK,
                    )