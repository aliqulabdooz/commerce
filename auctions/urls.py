from django.urls import path

from . import views

app_name = 'auctions'
urlpatterns = [
    path('', views.index, name="index"),
    path('category/<int:pk>/', views.product_category_list, name='product_category_list'),
    path('watchlist/', views.product_watchlist, name='product_watchlist'),
    path('add_product_watchlist/<int:pk>/', views.add_product_watchlist, name='add_product_watchlist'),
    path('remove_product_watchlist/<int:pk>/', views.remove_product_watchlist, name='remove_product_watchlist'),
    path('product_detail/<int:pk>/', views.product_detail, name='product_detail'),
    path('add_product/', views.add_product, name='add_product'),
    path('end_product_bid/<int:pk>/', views.end_product_bid, name='end_product_bid'),
    path('start_product_bid/<int:pk>/', views.start_product_bid, name='start_product_bid'),
    path('add_comment/<int:pk>/', views.add_comment, name='add_comment'),
]
