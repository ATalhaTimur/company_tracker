from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import AttendanceRecord
from datetime import datetime
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import logging


# Logger Ayarı
logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name='dispatch')
class CheckInAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        date = datetime.now().date()
        check_in_time = datetime.now().time()

        # Check-in kaydı kontrolü
        try:
            record = AttendanceRecord.objects.get(user=user, date=date)
            return Response({"error": "Check-in already recorded"}, status=400)
        except AttendanceRecord.DoesNotExist:
            # Yeni kayıt oluştur
            record = AttendanceRecord.objects.create(
                user=user,
                date=date,
                check_in_time=check_in_time
            )
            return Response({"message": "Check-in successful"}, status=201)


@method_decorator(csrf_exempt, name='dispatch')
class CheckOutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        date = datetime.now().date()
        check_out_time = datetime.now().time()

        try:
            record = AttendanceRecord.objects.get(user=user, date=date)
            if record.check_out_time:
                return Response({"error": "Check-out already recorded"}, status=400)

            # Check-out işlemini kaydet
            record.check_out_time = check_out_time
            record.save()
            return Response({"message": "Check-out successful"}, status=200)
        except AttendanceRecord.DoesNotExist:
            return Response({"error": "No check-in record found for today"}, status=404)
        except Exception as e:
            logger.error(f"Error during Check-Out: {str(e)}")
            return Response({"error": f"An error occurred: {str(e)}"}, status=500)


class AttendanceRecordsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        records = AttendanceRecord.objects.filter(user=user).values(
            'date', 'check_in_time', 'check_out_time', 'late_duration'
        )
        return Response(list(records), status=200)
