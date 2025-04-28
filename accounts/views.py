from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json

from analyzer.models import AnalysisResult


@csrf_exempt
def user_register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            email = data.get('email')
            if User.objects.filter(username=username).exists():
                return JsonResponse({'status': 'error', 'message': '用户名已存在'}, status=400)
            User.objects.create_user(username=username, password=password, email = email)
            return JsonResponse({'status': 'success', 'message': '注册成功'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': '无效的请求方法'}, status=405)


@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        try:
            # 解析 JSON 数据
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            # 验证用户
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'status': 'success', 'message': '登录成功'})
            else:
                return JsonResponse({'status': 'error', 'message': '用户名或密码错误'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    else:
        return JsonResponse({'status': 'error', 'message': '无效的请求方法'})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')

def root_view(request):
    if request.user.is_authenticated:
        return redirect('analyze')
    else:
        return redirect('login')


# def profile(request):
#     # 个人中心视图逻辑
#     return render(request, 'accounts/profile.html')

@login_required
def profile(request):
    user = request.user

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        user.email = email
        user.username = username
        user.first_name = "first_name"
        user.last_name = "last_name"
        user.save()

        messages.success(request, '用户信息更新成功！')
        return redirect('/')

    return render(request, 'accounts/profile.html', {'user': user})

# @login_required
# def datafile(request):
#     userId = request.user.id
#     results = AnalysisResult.objects.filter(user_id=userId).order_by('-created_at')
#     positive_count = AnalysisResult.objects.filter(user_id=userId, deepseek_label__icontains='positive').count()
#     negative_count = AnalysisResult.objects.filter(user_id=userId, deepseek_label__icontains='negative').count()
#     neutral_count = AnalysisResult.objects.filter(user_id=userId, deepseek_label__icontains='neutral').count()
#     return render(request, 'accounts/datafile.html', {
#         'results': results,
#         'positive_count': positive_count,
#         'negative_count': negative_count,
#         'neutral_count': neutral_count
#     })


@login_required
def datafile(request):
    userId = request.user.id
    results = AnalysisResult.objects.filter(user_id=userId).order_by('-created_at')
    positive_count = AnalysisResult.objects.filter(user_id=userId, deepseek_label__icontains='positive').count()
    negative_count = AnalysisResult.objects.filter(user_id=userId, deepseek_label__icontains='negative').count()
    neutral_count = AnalysisResult.objects.filter(user_id=userId, deepseek_label__icontains='neutral').count()

    # 计算情绪指数
    total_positive_negative = positive_count + negative_count
    emotion_index = (positive_count - negative_count) / total_positive_negative if total_positive_negative != 0 else 0

    return render(request, 'accounts/datafile.html', {
        'results': results,
        'positive_count': positive_count,
        'negative_count': negative_count,
        'neutral_count': neutral_count,
        'emotion_index': emotion_index
    })