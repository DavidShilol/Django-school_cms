from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from .forms import RegisterInfo 
from .models import DormAdminUser
from dorm.models import Student
from teacher.models import TeacherUser

# Create your views here.
def verify(**kwargs):
    if kwargs['password'] != kwargs['repeat_passwd']:
        return {'error': '两次密码输入不一致'}
    # print(kwargs)
    if DormAdminUser.objects.filter(idcard=kwargs['idcard']).exists() \
    or Student.objects.filter(idcard=kwargs['idcard']).exists() \
    or TeacherUser.objects.filter(idcard=kwargs['idcard']).exists():
        return {'error': '用户已注册'}
    else:
        return {'success': '可以注册'}

class RegisterView(View):
    def get(self, request):
        return render(request, 'dormadmin/register.html')

    def post(self, request):
        register_info = RegisterInfo(request.POST)
        if register_info.is_valid():
            data = register_info.clean()
            res = verify(**data)
            if res.get('error', ''):
                print(res.get('error', ''))
                context = {'error': res.get('error', '')}
                return render(request, 'dormadmin/register.html', context)
            else:
                print(res.get('success', ''))
                return redirect(reverse('dormadmin:register'))
        else:
            error_info = register_info.errors
            print(error_info)
            context = {'error': error_info}
            return render(request, 'dormadmin/register.html', context)
