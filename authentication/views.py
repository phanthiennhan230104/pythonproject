from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from mainapp.models import Account
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model

from django.contrib.auth.decorators import login_required, user_passes_test


User = get_user_model()

def home_view(request):
    return render(request, "authentication/homepage.html")

def send_otp_to_email(email, otp):
    subject = 'Xác thực tài khoản Django'
    message = f'Mã xác thực của bạn là: {otp}'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')
        email = request.POST.get('email')
        if password != confirmPassword:
            messages.error(request, "Password do not match.")
            return redirect('authentication:signup')

        otp = str(random.randint(100000, 999999))
        send_otp_to_email(email, otp)

        request.session['otp'] = otp
        request.session['temp_user'] = {
            'username': username,
            'password': password,
            'confirmPassword': confirmPassword,
            'email': email,
        }
        return redirect('authentication:verify_otp')
    return render(request, "authentication/register.html")

def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get('otp')
        session_otp = request.session.get('otp')
        user_data = request.session.get('temp_user')

        if entered_otp == session_otp and user_data:
            if User.objects.filter(username=user_data['username']).exists():
                messages.error(request, "Username already exists.")
                return redirect('authentication:signup')

            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password'],
                role_id=1,
            )

            user.save()
            Account.objects.create(
                user=user,
                is_email_verified=True,
                is_teacher=False
            )

            request.session.pop('otp')
            request.session.pop('temp_user')

            messages.success(request, "Email verified successfully. Please sign in.")
            return redirect('authentication:signin')
        else:
            messages.error(request, "Invalid OTP.")
            return redirect('authentication:verify_otp')

    return render(request, "authentication/verify_otp.html")

def signin(request):
    if request.user.is_authenticated:
        try:
            account = request.user.account
            if account.is_teacher:
                return redirect('authentication:teacher_homepage')
            else:
                return redirect('authentication:student_homepage')
        except Account.DoesNotExist:
            logout(request)
            return redirect('authentication:signin')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:

            login(request, user)

            if user.is_superuser:
                return redirect('authentication:admin_homepage')
            try:
                account = user.account
                if not account.is_email_verified:
                    messages.error(request, "Please verify your email before signing in.")
                    return redirect('authentication:signup')
            except Account.DoesNotExist:
                messages.error(request, "Account data error. Please contact admin.")
                return redirect('authentication:signin')

            login(request, user)

            if account.is_teacher:
                return redirect('authentication:teacher_homepage')
            else:
                return redirect('authentication:student_homepage')
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('authentication:signin')

    return render(request, "authentication/login.html")

def teacher_homepage(request):
    if not request.user.is_authenticated:
        return redirect('authentication:signin')
    try:
        account = request.user.account
        if not account.is_teacher:
            return redirect('authentication:student_homepage')
    except Account.DoesNotExist:
        return redirect('authentication:signin')
    return render(request, "authentication/homepage_gv.html")

def student_homepage(request):
    if not request.user.is_authenticated:
        return redirect('authentication:signin')
    try:
        account = Account.objects.get(user=request.user)
        if account.is_teacher:
            return redirect('authentication:teacher_homepage')
    except Account.DoesNotExist:
        return redirect('authentication:signin')
    return render(request, "authentication/homepage_hs.html")

@login_required 
@user_passes_test(lambda user : user.is_superuser)

def admin_homepage(request):
    return render(request, "authentication/homepage_admin.html")

