from django.contrib import admin
from .models import Book, Review, Rating, Category , Cart, CartItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'price', 'stock', 'average_rating', 'review_count', 'created_at']
    list_filter = ['category', 'author', 'created_at']
    search_fields = ['title', 'author', 'isbn']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'author', 'category', 'isbn')
        }),
        ('جزئیات', {
            'fields': ('description', 'pages', 'publication_date', 'cover_image')
        }),
        ('قیمت و موجودی', {
            'fields': ('price', 'stock')
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at')
        }),
    )

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'short_comment', 'created_at']
    list_filter = ['created_at', 'book']
    search_fields = ['user__username', 'book__title', 'comment']
    
    def short_comment(self, obj):
        return obj.comment[:50] + '...' if len(obj.comment) > 50 else obj.comment
    short_comment.short_description = 'نظر'

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'score', 'created_at']
    list_filter = ['score', 'created_at']
    search_fields = ['user__username', 'book__title']
    
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['added_at']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_total_items', 'get_total_price', 'created_at']
    inlines = [CartItemInline]
    
    def get_total_items(self, obj):
        return obj.get_total_items()
    get_total_items.short_description = 'تعداد آیتم‌ها'
    
    def get_total_price(self, obj):
        return f'{obj.get_total_price():,} تومان'
    get_total_price.short_description = 'مجموع قیمت'

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'book', 'quantity', 'get_total_price', 'added_at']
    list_filter = ['added_at']
    
    def get_total_price(self, obj):
        return f'{obj.get_total_price():,} تومان'
    get_total_price.short_description = 'قیمت کل'