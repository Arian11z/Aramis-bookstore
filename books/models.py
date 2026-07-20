from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from .hazm_sentiment import HazmSentimentAnalyzer
from hazm import sent_tokenize, word_tokenize, Normalizer
from hazm.utils import stopwords_list
from collections import Counter


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='نام دسته')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='اسلاگ')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'دسته‌بندی'
        verbose_name_plural = 'دسته‌بندی‌ها'
        ordering = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان کتاب')
    author = models.CharField(max_length=100, verbose_name='نویسنده')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='books', verbose_name='دسته‌بندی')
    description = models.TextField(verbose_name='توضیحات')
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='قیمت (تومان)')
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True, verbose_name='تصویر جلد')
    publication_date = models.DateField(verbose_name='تاریخ انتشار')
    isbn = models.CharField(max_length=13, unique=True, verbose_name='شابک (ISBN)')
    pages = models.IntegerField(verbose_name='تعداد صفحات')
    stock = models.IntegerField(default=0, verbose_name='موجودی انبار')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    class Meta:
        verbose_name = 'کتاب'
        verbose_name_plural = 'کتاب‌ها'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return round(sum([r.score for r in ratings]) / ratings.count(), 1)
        return 0

    def review_count(self):
        return self.reviews.count()


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews', verbose_name='کتاب')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    comment = models.TextField(verbose_name='نظر')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'
        ordering = ['-created_at']
        unique_together = ['book', 'user']

    def __str__(self):
        return f'{self.user.username} - {self.book.title}'
    
    def get_sentiment(self):
        analyzer = HazmSentimentAnalyzer()
        sentiment, confidence = analyzer.analyze(self.comment)
        return {
            'sentiment': sentiment,
            'confidence': confidence,
            'label': analyzer.get_sentiment_label(sentiment),
        }
    

class Rating(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='ratings', verbose_name='کتاب')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='امتیاز (1 تا 5)'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')

    class Meta:
        verbose_name = 'امتیاز'
        verbose_name_plural = 'امتیازها'
        unique_together = ['book', 'user']

    def __str__(self):
        return f'{self.user.username} - {self.book.title} - {self.score} ستاره'
    
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='کاربر')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبدهای خرید'

    def __str__(self):
        return f'سبد خرید {self.user.username}'

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())

    def get_total_items(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name='سبد خرید')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='کتاب')
    quantity = models.PositiveIntegerField(default=1, verbose_name='تعداد')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ افزودن')

    class Meta:
        verbose_name = 'آیتم سبد خرید'
        verbose_name_plural = 'آیتم‌های سبد خرید'
        unique_together = ['cart', 'book']

    def __str__(self):
        return f'{self.quantity} x {self.book.title}'

    def get_total_price(self):
        return self.quantity * self.book.price