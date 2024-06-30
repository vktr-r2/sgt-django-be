from django.shortcuts import render
from call_caddy.services.schedule_call import ScheduleCallService

# Create your views here.

def login_view(request):
    # Your view logic here

    service_instance = ScheduleCallService()
    json_string = service_instance.get_schedule(org_id="1")
    context = {
        'schedule_data': json_string
        }
    return render(request, 'login.html', context)