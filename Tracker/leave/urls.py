from django.urls import path
from .views import LeaveRequestView, MyLeaveRequestsView, ApproveLeaveView
from .api_views import LeaveRequestAPIView, MyLeaveRequestsAPIView, ApproveLeaveAPIView

urlpatterns = [
    path('request/', LeaveRequestView.as_view(), name='api-leave-request'),
    path('my-requests/', MyLeaveRequestsView.as_view(), name='api-my-leave-requests'),
    path('approvals/', ApproveLeaveView.as_view(), name='api-leave-approvals'),
    path('api/request/', LeaveRequestAPIView.as_view(), name='api-leave-request'),
    path('api/my-requests/', MyLeaveRequestsAPIView.as_view(), name='api-my-leave-requests'),
    path('api/approve/', ApproveLeaveAPIView.as_view(), name='api-approve-leave'),

]
