from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from .forms import SignUpForm

def sign(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '회원가입에 성공했습니다. 로그인 페이지로 이동합니다.')
            return redirect('personaccounts:sign')
        else:
            messages.error(request, '회원가입에 실패했습니다. 오류를 수정하고 다시 시도해주세요.')
    else:
        form = SignUpForm()
    return render(request, 'sign.html', {'form': form, 'login_form': AuthenticationForm()})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, '로그인에 성공했습니다.')
                return redirect(reverse('chatgpt:chat'))
            else:
                messages.error(request, '유효하지 않은 사용자명 또는 비밀번호입니다.')
                return redirect('personaccounts:sign')
        else:
            messages.error(request, '유효하지 않은 사용자명 또는 비밀번호입니다.')
            return redirect('personaccounts:sign')
    else:
        return redirect('personaccounts:sign')

def logout_view(request):
    logout(request)
    messages.success(request, '로그아웃 되었습니다.')
    return redirect('home')

