from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('book/<int:pk>/review/', views.add_review, name='add_review'),
    path('book/<int:pk>/rating/', views.add_rating, name='add_rating'),
    path('category/<slug:slug>/', views.category_books, name='category_books'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:pk>/', views.update_cart_item, name='update_cart_item'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('my-admin/', views.admin_dashboard, name='admin_dashboard'),
]
