from django.contrib import admin
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name',)
    ordering = ('category_name',)
    search_fields = ('category__name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'starting_bid',)
    ordering = ('date_created',)
    search_fields = ('product_name',)
    list_filter = ('date_created', 'date_modified', 'status',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    ...


@admin.register(WinnerBid)
class WinnerBidAdmin(admin.ModelAdmin):
    list_display = ('author__username',)


@admin.register(WatchList)
class WatchListAdmin(admin.ModelAdmin):
    list_display = ('author__username',)
