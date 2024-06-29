from django.shortcuts import render

# Create your views here.

def login_view(request):
    # Your view logic here
    context = {
        'data_to_pass_to_template': 'Hello from your view!',
    }
    return render(request, 'login.html', context)