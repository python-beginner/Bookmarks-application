from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Link, Tag, Bookmark
from .forms import LoginForm, RegistrationForm, BookmarkForm, SearchForm


def main_page(request):
    return render(request, 'bookmarks/main_page.html')


def user_page(request, username):
    user = get_object_or_404(User, username=username)
    bookmarks = user.bookmarks.all()
    context = {
        'bookmarks': bookmarks,
        'show_tags': True
    }
    return render(request, 'bookmarks/user_page.html', context=context)


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                if 'next' in request.session:
                    next = request.session['next']
                    del request.session['next']
                    return HttpResponseRedirect(next)
                return HttpResponseRedirect(reverse('main_page'))
            else:
                error = 'invalid username or password'
        else:
            error = None
    else:
        form = LoginForm()
        error = None
        request.session['next'] = request.GET.get('next')
    return render(request, 'bookmarks/user_login.html', {'form': form, 'error': error})


def user_logout(request):
    user = request.user
    logout(request)
    return HttpResponseRedirect(reverse('main_page'))


def user_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            login(request, user)
            return HttpResponseRedirect(reverse('main_page'))
    else:
        form = RegistrationForm()

    return render(request, 'bookmarks/user_register.html', {'form': form})


@login_required
def bookmark_save(request):
    if request.method == 'POST':
        form = BookmarkForm(request.POST)
        if form.is_valid():
            # Create or get the link
            link, created = Link.objects.get_or_create(
                url=form.cleaned_data['url']
            )
            # Create or get the bookmark
            bookmark, dummy = Bookmark.objects.get_or_create(
                user=request.user,
                link=link
            )
            # Update the bookmark title
            bookmark.title = form.cleaned_data['title']
            # If updated clear the tags
            if not created:
                bookmark.tags.clear()
                tag_names = form.cleaned_data['tags'].split()
                for tag_name in tag_names:
                    tag, dummy = Tag.objects.get_or_create(title=tag_name)
                    bookmark.tags.add(tag)
                bookmark.save()
                return HttpResponseRedirect(reverse('main_page'))
    else:
        form = BookmarkForm()
    return render(request, 'bookmarks/bookmark_form.html', {'form': form})


def tag_page(request, tag_name):
    tag = get_object_or_404(Tag, title=tag_name)
    bookmarks = tag.bookmarks.all()
    context = {
        'tag': tag,
        'show_tags': True,
        'show_user': True,
        'bookmarks': bookmarks,
    }
    return render(request, 'bookmarks/tag_page.html', context=context)


def tag_cloud_page(request):
    MAX_WEIGHT = 5
    tags = Tag.objects.order_by('title')
    # Calculate tag, min and max counts.
    min_count = max_count = tags[0].bookmarks.count()
    for tag in tags:
        tag.count = tag.bookmarks.count()
        if tag.count < min_count:
            min_count = tag.count
        if max_count < tag.count:
            max_count = tag.count
    # Calculate count range. Avoid dividing by zero.
    range = float(max_count - min_count)
    if range == 0.0:
        range = 1.0
    # Calculate tag weights.
    for tag in tags:
        tag.weight = int(MAX_WEIGHT * (tag.count - min_count) / range)
    return render(request, 'bookmarks/tag_cloud_page.html', {'tags': tags})


def search_page(request):
    form = SearchForm()
    bookmarks = []
    error = None
    show_results = False
    if request.GET.get('query'):
        show_results = True
        query = request.GET.get('query').strip()
        form = SearchForm({'query': query})
        bookmarks = Bookmark.objects.filter(title__icontains=query)[:10]
        if not bookmarks:
            error = 'No bookmarks with this title'
        else:
            error = None
    context = {
        'form': form,
        'bookmarks': bookmarks,
        'show_results': show_results,
        'show_user': True,
        'show_tags': True,
        'error': error,
    }
    if request.GET.get('ajax') is not None:
        print('ajax')
        return render(request, 'bookmark_list.html', context=context)
    else:
        return render(request, 'bookmarks/search.html', context=context)
