from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import AddProductForm, BidForm, AddCommentForm
from .models import *


def index(request):
    products = Product.objects.all().order_by('-date_created')
    category = Category.objects.all()
    context = {
        'products': products,
        'category': category,
    }
    return render(request, 'index.html', context)


def product_category_list(request, pk):
    products = Product.objects.filter(category_id=pk).order_by('-date_created')
    category = Category.objects.get(id=pk)
    context = {
        'products': products,
        'category': category,
    }
    return render(request, 'auctions/product_category_list.html', context)


def add_product_watchlist(request, pk):
    try:
        watch = WatchList.objects.get(author_id=request.user.id)
        watch.product.add(pk)
    except WatchList.DoesNotExist:
        watch = WatchList.objects.create(author_id=request.user.id)
        watch.save()
        watch.product.add(pk)
    messages.success(request, 'watchlist successfully added')
    return redirect('auctions:product_detail', pk)


def product_watchlist(request):
    products = []
    if not request.user.is_authenticated:
        messages.warning(request, 'you are not login')
        return redirect('accounts:login')
    watch_lists = CustomUser.objects.get(id=request.user.id).user_watchlist.all()
    for watch in watch_lists:
        products.extend(watch.product.all())
    context = {
        'watch_lists': products,
    }
    return render(request, 'auctions/watchlist.html', context)


def product_detail(request, pk):
    product = Product.objects.get(id=pk)
    try:
        winner = WinnerBid.objects.get(product_id=pk)
    except WinnerBid.DoesNotExist:
        winner = None
    bid_form = BidForm(request.POST or None)
    comment_form = AddCommentForm()
    if bid_form.is_valid():
        bid = bid_form.cleaned_data['starting_bid']
        if bid < product.starting_bid:
            messages.error(request, f'your bid at the rate of {bid} is litter than {product.starting_bid}')
        else:
            product.starting_bid = bid
            request.session['user'] = request.user.id
            product.save()
            messages.success(request, f'your bid at the rate of {bid} was successfully registered.')
        return redirect(product.get_absolute_url())
    check_user_product = product.author.id == request.user.id
    try:
        check_watchlist_product = CustomUser.objects.get(id=request.user.id).user_watchlist.get(
            product=product).product.all()
    except WatchList.DoesNotExist:
        check_watchlist_product = False
    context = {
        'product': product,
        'bid_form': bid_form,
        'check': check_user_product,
        'check_watch': check_watchlist_product,
        'comment_form': comment_form,
        'winner': winner,
        'comments': product.product_comment.all(),
    }
    return render(request, 'auctions/product_detail.html', context)


def add_product(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'you are not login')
        return redirect('accounts:login')
    form = AddProductForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.author = request.user
        instance.save()
        messages.success(request, 'product successfully added')
        return redirect('auctions:index')
    context = {
        'form': form,
    }
    return render(request, 'auctions/add_product.html', context)


def remove_product_watchlist(request, pk):
    product = Product.objects.get(id=pk)
    watch = WatchList.objects.get(author_id=request.user.id)
    watch.product.remove(product)
    messages.success(request, 'your watchlist is removed')
    return redirect(product.get_absolute_url())


def add_comment(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, 'you must be logged in')
        return redirect('accounts:login')
    comment = AddCommentForm(request.POST)
    product = Product.objects.get(id=pk)
    if comment.is_valid():
        instance = comment.save(commit=False)
        instance.author = request.user
        instance.save()
        instance.product.add(product)
        messages.success(request, 'added comment successfully')
    return redirect(product.get_absolute_url())


def start_product_bid(request, pk):
    product = Product.objects.get(id=pk)
    product.status = 'start'
    product.save()
    WinnerBid.objects.filter(product_id=pk).delete()
    request.session['user'] = request.user.id
    messages.success(request, f'starting bid at {product.starting_bid}')
    return redirect(product.get_absolute_url())


def end_product_bid(request, pk):
    product = Product.objects.get(id=pk)
    if 'user' in request.session and request.session['user'] != request.user.id:
        winner = WinnerBid.objects.create(author_id=request.session['user'], product_id=product.id)
        winner.save()
    product.status = 'end'
    product.save()
    messages.success(request, f'ending bid at {product.starting_bid}')
    return redirect(product.get_absolute_url())
