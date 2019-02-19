from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from .forms import RegisterInfo, LoginInfo 
from .models import DormAdminUser
from dorm.models import Student
from teacher.models import TeacherUser
import random

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
                context = {'error': res.get('error', '')}
                return render(request, 'dormadmin/register.html', context)
            else:
                workid = str(random.randint(10000000, 99999999))
                user = DormAdminUser(
                        name=data.get('name', ''),
                        sex=data.get('sex', ''),
                        idcard=data.get('idcard', ''),
                        password=data.get('password', ''),
                        phone=data.get('phone', ''),
                        workid=workid)
                user.save()
                return redirect(reverse('dormadmin:login'))
        else:
            error_info = register_info.errors.get_json_data()
            error = ['{}:{}'.format(k, v[0].get('message', '')) for k, v in error_info.items()]
            context = {'error': '\\n'.join(error)}
            return render(request, 'dormadmin/register.html', context)

class LoginView(View):
    def get(self, request):
        return render(request, 'dormadmin/login.html')

    def post(self, request):
        login_info = LoginInfo(request.POST)
        if login_info.is_valid():
            data = login_info.clean()
            if DormAdminUser.objects.filter(
                    workid=data.get('workid', ''),
                    password=data.get('password', '')
                    ).exists():
                request.session['workid'] = data.get('workid', '')
                return redirect(reverse('dormadmin:index'))
            else:
                context = {'error': '用户或密码错误'}
                return render(request, 'dormadmin/login.html', context)
        else:
            error_info = login_info.errors.get_json_data()
            error = ['{}:{}'.format(k, v[0].get('message', '')) for k, v in error_info.items()]
            context = {'error': '\\n'.join(error)}
            return render(request, 'dormadmin/login.html', context)

class IndexView(View):
    def get(self, request):
        workid = request.session.get('workid', '')
        print(workid)
        return render(request, 'dormadmin/index.html')

    def post(self, request):
        pass
