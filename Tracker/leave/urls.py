from django.urls import path
from .views import LeaveRequestView, MyLeaveRequestsView, ApproveLeaveView

urlpatterns = [
    path('request/', LeaveRequestView.as_view(), name='api-leave-request'),
    path('my-requests/', MyLeaveRequestsView.as_view(), name='api-my-leave-requests'),
    path('approvals/', ApproveLeaveView.as_view(), name='api-leave-approvals'),
]
