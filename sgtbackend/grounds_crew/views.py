from django.shortcuts import render
from call_caddy.services.leaderboard_call import LeaderboardCallService

# Create your views here.

def login_view(request):
    # Your view logic here

    service_instance = LeaderboardCallService()
    json_string = service_instance.get_leaderboard(org_id="1", tourn_id="100")
    context = {
        'leaderboard_data': json_string
        }
    return render(request, 'login.html', context)