from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from leave.models import LeaveRequest
from django.utils.dateparse import parse_date


class LeaveRequestView(LoginRequiredMixin, TemplateView):
    template_name = "leave/leave_request.html"

    def post(self, request, *args, **kwargs):
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        reason = request.POST.get("reason", "")

        if not start_date or not end_date:
            messages.error(request, "Start and end dates are required!")
            return redirect('leave-request')

        try:
            start_date_parsed = parse_date(start_date)
            end_date_parsed = parse_date(end_date)

            if not start_date_parsed or not end_date_parsed:
                messages.error(request, "Invalid date format, please use a valid date!")
                return redirect('leave-request')

            if start_date_parsed > end_date_parsed:
                messages.error(request, "Start date cannot be after end date!")
                return redirect('leave-request')

            LeaveRequest.objects.create(
                user=request.user,
                start_date=start_date_parsed,
                end_date=end_date_parsed,
                reason=reason
            )
            messages.success(request, "Leave request submitted successfully!")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
        return redirect('leave-request')


class MyLeaveRequestsView(LoginRequiredMixin, TemplateView):
    template_name = "leave/my_leave_requests.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['leave_requests'] = LeaveRequest.objects.filter(user=self.request.user)
        return context


class ApproveLeaveView(LoginRequiredMixin, TemplateView):
    template_name = "leave/approve_leave.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.role == "manager":
            context['leave_requests'] = LeaveRequest.objects.filter(status="pending").select_related('user')
        return context

    def post(self, request, *args, **kwargs):
        leave_id = request.POST.get("leave_id")
        action = request.POST.get("action")

        if action not in ["approve", "reject"]:
            messages.error(request, "Invalid action!")
            return redirect('leave-approvals')

        try:
            leave_request = LeaveRequest.objects.get(id=leave_id, status="pending")
            leave_request.status = action
            leave_request.save()
            messages.success(request, f"Leave request {action}d successfully.")
        except LeaveRequest.DoesNotExist:
            messages.error(request, "Leave request not found or already processed.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
        return redirect('leave-approvals')
