from click_count_api.serializers import ClickCountSerializer
from django.db.models import  Sum, F
from rest_framework import views, status
from rest_framework.response import Response
from click_count_api.models import ClickCount
from django.http import JsonResponse

class ClickModelView(views.APIView):

    def post(self, request):
        ip_address = request.data.get("ip","").strip()
        currentCount = request.data.get("currentCount",0)
        city = request.data.get("city","Anonmyous").strip()
        country = request.data.get("country","Anonmyous").strip()
        if currentCount == 0:
            return JsonResponse({"success": True, "message": "click count zero"}, status=200)
        if not ip_address:
            obj, created = ClickCount.objects.get_or_create(country="Anonymous", city="Anonymous",
                                                        defaults={"count": 0})
            obj.count = F("count") + currentCount
            obj.save()
        else:
            obj, created = ClickCount.objects.get_or_create(country=country, city=city, defaults={"count": currentCount})
            obj.count = F("count") + currentCount
            obj.save()

        message = "Click updated successfully" if not created else "Click recorded successfully"
        return JsonResponse({"success": True, "message": message}, status=200)
    

    def get(self, request):
        queryset = ClickCount.objects.all()
        if queryset:
            queryset = queryset.order_by('-count')
            total_count = queryset.aggregate(Sum("count"))['count__sum'] 
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