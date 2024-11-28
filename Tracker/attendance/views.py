from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import AttendanceRecord
from datetime import datetime

class CheckInView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        date = datetime.now().date()
        check_in_time = datetime.now().time()

        record, created = AttendanceRecord.objects.get_or_create(user=user, date=date)
        if not created:
            return Response({"error": "Check-in already recorded"}, status=400)

        record.check_in_time = check_in_time
        record.save()
        return Response({"message": "Check-in successful"}, status=201)

class CheckOutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        date = datetime.now().date()

        try:
            record = AttendanceRecord.objects.get(user=user, date=date)
        except AttendanceRecord.DoesNotExist:
            return Response({"error": "No check-in record found for today"}, status=404)

        record.check_out_time = datetime.now().time()
        record.save()
        return Response({"message": "Check-out successful"}, status=200)

class AttendanceRecordsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        records = AttendanceRecord.objects.filter(user=user).values('date', 'check_in_time', 'check_out_time', 'late_duration')
        return Response(records, status=200)
