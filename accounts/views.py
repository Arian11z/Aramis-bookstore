from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm
from books.models import Review, Rating

def register_view(request):
    if request.user.is_authenticated:
        return redirect('books:book_list')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'خوش آمدید {user.username}! حساب شما با موفقیت ساخته شد.')
            return redirect('books:book_list')
        else:
            messages.error(request, 'لطفاً خطاهای فرم را اصلاح کنید.')
    else:
        form = RegisterForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('books:book_list')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'خوش آمدید {username}!')
                return redirect('books:book_list')
        else:
            messages.error(request, 'نام کاربری یا رمز عبور اشتباه است.')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'شما با موفقیت خارج شدید.')
    return redirect('books:book_list')

@login_required
def profile_view(request):
    user_reviews = Review.objects.filter(user=request.user).select_related('book')
    user_ratings = Rating.objects.filter(user=request.user).select_related('book')
    
    context = {
        'user_reviews': user_reviews,
        'user_ratings': user_ratings,
    }
    return render(request, 'accounts/profile.html', context)