from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, reverse
from django.views.generic import View, ListView, DetailView
from .forms import RegisterInfo, LoginInfo 
from .models import DormAdminUser
from dorm.models import Building, Room, Student
from teacher.models import TeacherUser
import random
from django.db.models import F

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

def login_judge(request):
    if request.session.get('workid', '') \
    and request.session.get('workname', ''):
        return True
    else:
        return False

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
                q = DormAdminUser.objects.get(workid=data.get('workid', ''))
                request.session['workname'] = q.name
                return redirect(reverse('dormadmin:index'))
            else:
                context = {'error': '用户或密码错误'}
                return render(request, 'dormadmin/login.html', context)
        else:
            error_info = login_info.errors.get_json_data()
            error = ['{}:{}'.format(k, v[0].get('message', '')) for k, v in error_info.items()]
            context = {'error': '\\n'.join(error)}
            return render(request, 'dormadmin/login.html', context)

def LogoutView(request):
    del request.session['workid']
    del request.session['workname']
    return redirect(reverse('dormadmin:login'))

class IndexView(View):
    def get(self, request):
        if not login_judge(request):
            return redirect(reverse('dormadmin:login'))
        workid = request.session.get('workid', '')
        workname = request.session.get('workname', '')
        context = {'workstatus': '{}#{}'.format(workname, workid)}
        return render(request, 'dormadmin/index.html', context)

    def post(self, request):
        pass

class BuildingView(ListView):
    template_name = 'dormadmin/building.html'
    context_object_name = 'building_list'

    def get_queryset(self):
        return Building.objects.all()

class RoomView(ListView):
    template_name = 'dormadmin/room.html'
    context_object_name = 'room_list'

    def get_queryset(self):
        return Room.objects\
                .annotate(building_num=F('building__number'))\
                .filter(building_num=self.kwargs.get('building_num', ''))\
                .order_by('number')

class StudentView(ListView):
    template_name = 'dormadmin/student.html'
    context_object_name = 'student_list'

    def get_queryset(self):
        return Student.objects\
                .annotate(room_num=F('room__number'), 
                building_num=F('room__building__number'),
                teacher_name=F('teacher__name'))\
                .filter(room_num=self.kwargs.get('room_num', ''),
                        building_num=self.kwargs.get('building_num', ''))

class SearchView(View):
    def get(self, request):
        print('get!')
        return render(request, 'dormadmin/search.html')

    def post(self, request):
        if request.is_ajax():
            key = request.POST.get('key', 'none')
            key = key if key else 'none'
            data = Student.objects\
                    .annotate(room_num=F('room__number'),
                    building_num=F('room__building__number'),
                    teacher_name=F('teacher__name'))\
                    .filter(name__contains=key)\
                    .order_by('number')
            student_list = []
            for x in data:
                student = {}
                student['number'] = x.number
                student['name'] = x.name
                student['info'] = x.info
                student['teacher'] = str(x.teacher)
                student['room'] = str(x.room)
                student_list.append(student)
            return JsonResponse({'student_list': student_list})
        return render(request, 'dormadmin/search.html')
