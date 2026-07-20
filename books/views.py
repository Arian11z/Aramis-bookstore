from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required ,user_passes_test
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Book, Review, Rating, Category, Cart, CartItem
from .forms import ReviewForm, RatingForm

def book_list(request):
    books = Book.objects.all()
    
    search_query = request.GET.get('search', '')
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    author_filter = request.GET.get('author', '')
    if author_filter:
        books = books.filter(author__icontains=author_filter)
    
    category_filter = request.GET.get('category', '')
    if category_filter:
        books = books.filter(category__slug=category_filter)
    
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    
    if min_price:
        books = books.filter(price__gte=min_price)
    if max_price:
        books = books.filter(price__lte=max_price)
    
    min_rating = request.GET.get('min_rating', '')
    if min_rating:
        books = [book for book in books if book.average_rating() >= float(min_rating)]
    
    sort_by = request.GET.get('sort', 'newest')
    
    if sort_by == 'newest':
        books = books if isinstance(books, list) else books.order_by('-created_at')
    elif sort_by == 'oldest':
        books = books if isinstance(books, list) else books.order_by('created_at')
    elif sort_by == 'price_low':
        books = books if isinstance(books, list) else books.order_by('price')
    elif sort_by == 'price_high':
        books = books if isinstance(books, list) else books.order_by('-price')
    elif sort_by == 'title':
        books = books if isinstance(books, list) else books.order_by('title')
    
    if not isinstance(books, list):
        paginator = Paginator(books, 9)
        page_number = request.GET.get('page')
        books = paginator.get_page(page_number)
    
    authors = Book.objects.values_list('author', flat=True).distinct()
    categories = Category.objects.all()
    
    context = {
        'books': books,
        'authors': authors,
        'categories': categories,
        'search_query': search_query,
        'author_filter': author_filter,
        'category_filter': category_filter,
        'min_price': min_price,
        'max_price': max_price,
        'min_rating': min_rating,
        'sort_by': sort_by,
    }
    return render(request, 'books/book_list.html', context)

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reviews = book.reviews.all()
    
    user_review = None
    user_rating = None
    
    if request.user.is_authenticated:
        user_review = Review.objects.filter(book=book, user=request.user).first()
        user_rating = Rating.objects.filter(book=book, user=request.user).first()
    
    review_form = ReviewForm()
    rating_form = RatingForm()
    
    if user_rating:
        rating_form = RatingForm(instance=user_rating)
    
    context = {
        'book': book,
        'reviews': reviews,
        'review_form': review_form,
        'rating_form': rating_form,
        'user_review': user_review,
        'user_rating': user_rating,
    }
    return render(request, 'books/book_detail.html', context)

@login_required
def add_review(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            existing_review = Review.objects.filter(book=book, user=request.user).first()
            
            if existing_review:
                messages.warning(request, 'شما قبلاً برای این کتاب نظر ثبت کرده‌اید.')
            else:
                review = form.save(commit=False)
                review.book = book
                review.user = request.user
                review.save()
                messages.success(request, 'نظر شما با موفقیت ثبت شد!')
    
    return redirect('books:book_detail', pk=pk)

@login_required
def add_rating(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        existing_rating = Rating.objects.filter(book=book, user=request.user).first()
        
        if existing_rating:
            form = RatingForm(request.POST, instance=existing_rating)
        else:
            form = RatingForm(request.POST)
        
        if form.is_valid():
            rating = form.save(commit=False)
            rating.book = book
            rating.user = request.user
            rating.save()
            messages.success(request, 'امتیاز شما با موفقیت ثبت شد!')
    
    return redirect('books:book_detail', pk=pk)

def category_books(request, slug):
    category = get_object_or_404(Category, slug=slug)
    books = Book.objects.filter(category=category)
    
    paginator = Paginator(books, 9)
    page_number = request.GET.get('page')
    books = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'books': books,
    }
    return render(request, 'books/category_books.html', context)

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all().select_related('book')
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'books/cart.html', context)

@login_required
def add_to_cart(request, pk):
    book = get_object_or_404(Book, pk=pk)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)
    
    if not created:
        if cart_item.quantity < book.stock:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, f'تعداد "{book.title}" در سبد خرید افزایش یافت.')
        else:
            messages.warning(request, f'موجودی "{book.title}" کافی نیست.')
    else:
        if book.stock > 0:
            messages.success(request, f'"{book.title}" به سبد خرید اضافه شد.')
        else:
            cart_item.delete()
            messages.error(request, f'"{book.title}" موجود نیست.')
    
    return redirect('books:book_detail', pk=pk)

@login_required
def remove_from_cart(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)
    book_title = cart_item.book.title
    cart_item.delete()
    messages.info(request, f'"{book_title}" از سبد خرید حذف شد.')
    return redirect('books:cart')

@login_required
def update_cart_item(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'increase':
            if cart_item.quantity < cart_item.book.stock:
                cart_item.quantity += 1
                cart_item.save()
                messages.success(request, 'تعداد افزایش یافت.')
            else:
                messages.warning(request, 'موجودی کافی نیست.')
        
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
                messages.success(request, 'تعداد کاهش یافت.')
            else:
                cart_item.delete()
                messages.info(request, 'کتاب از سبد خرید حذف شد.')
    
    return redirect('books:cart')

@login_required
def clear_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart.items.all().delete()
    messages.info(request, 'سبد خرید خالی شد.')
    return redirect('books:cart')

def about_view(request):
    return render(request, 'books/about.html')

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        messages.success(request, 'پیام شما با موفقیت ارسال شد. به زودی با شما تماس خواهیم گرفت.')
        return redirect('books:contact')
    
    return render(request, 'books/contact.html')

def is_admin(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_admin)
def admin_dashboard(request):
    context = {
        'user': request.user
    }
    return render(request, 'books/admin_dashboard.html', context)
