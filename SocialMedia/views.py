import cv2
import os
from .models import Post, Comment, Image, User
from django.shortcuts import get_object_or_404
from .forms import PostForm, CommentForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.conf import settings

def HomePage(request):
    return render(request, 'index.html')

@login_required
def ShowAllPosts(request):
    post_list = Post.objects.all()


    paginator = Paginator(post_list, 8) 

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    
    context = {'page_obj': page_obj, 'posts': page_obj}

    return render(request, 'posts.html', context)

@login_required
def search_posts(request):
    query = request.GET.get('q')
    post_list = Post.objects.none()
    if query:
        post_list = Post.objects.filter(Q(title__icontains=query) | Q(text__icontains=query) | Q(author__username__icontains=query))
    
    paginator = Paginator(post_list, 8)  

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj, 'posts': post_list}

    return render(request, 'posts.html', context)

@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            
            images = request.FILES.getlist('images')
            for img in images:
                # Save the image to a temporary file
                file_path = os.path.join(settings.MEDIA_ROOT, 'temp', img.name)
                with open(file_path, 'wb') as f:
                    for chunk in img.chunks():
                        f.write(chunk)

                image = cv2.imread(file_path)
                resized_image = cv2.resize(image, (600, 600), interpolation=cv2.INTER_AREA)
  
                image_name = img.name.split('.')[0] + '_resized.jpg'
                image_path = os.path.join(settings.MEDIA_ROOT, 'images', image_name)
                cv2.imwrite(image_path, resized_image, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
                image_obj = Image(post=post, image='images/' + image_name)
                image_obj.save()
                os.remove(file_path)
            
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'MakeNewPost.html', {'form': form})


@login_required
def post_detail(request, pk):
    form = CommentForm()
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment was added successfully.')
            return redirect('post_detail', pk=post.pk)
        else:
            messages.error(request, 'There was an error adding your comment. Please try again.')
    else:
        form = CommentForm()
    comments = Comment.objects.filter(post=post)
    context = {'post': post, 'comments': comments, 'form': form}
    return render(request, 'post_detail.html', context)

@login_required
def like_post(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        post.likes += 1
        post.save()
        data = {
            'likes': post.likes
        }
        return JsonResponse(data)

@login_required
def dislike_post(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        post.dislikes += 1
        post.save()
        data = {
            'dislikes': post.dislikes
        }
        return JsonResponse(data)

@login_required
def my_posts(request):
    post_list = Post.objects.filter(author=request.user)
    context = {'posts': post_list}
    return render(request, 'my_posts.html', context)

@login_required
def delete_a_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        if request.user == post.author:
            post.delete()
        else:
            return redirect('my_posts')
    return redirect('my_posts')

@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form})

@login_required
def user_profile_settings(request):

    return render(request, 'settings.html')

@login_required
def view_user_profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    Posts = Post.objects.filter(author=user).order_by('-likes')[:5]

    context = {"CurrentUser": user, "posts": Posts}
    return render(request, 'user_profile.html', context=context)

@login_required
def delete_user_account(request, pk):
    if request.method == 'POST':
        if request.user == get_object_or_404(User, pk=pk):
            user = get_object_or_404(User, pk=pk)
            user.delete()
            return redirect('HomePage')
        

