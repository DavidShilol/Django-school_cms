from django.shortcuts import render

# Create your views here.
def LoginView(request):
    return render(request, 'dorm/login.html')

def RegisterView(request):
    return render(request, 'dorm/register.html')

