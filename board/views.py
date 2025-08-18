from django.shortcuts import render, redirect, get_object_or_404
from .models import Post  
from .forms import PostForm
import os
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'board/post_detail.html', {'post': post})

def board_view(request):
    post_list = Post.objects.order_by('-created_at')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page', 1)
    posts = paginator.get_page(page_number)

    # 번호 계산 후 각 post 객체에 주입
    start_index = paginator.count - (posts.number - 1) * paginator.per_page
    for idx, post in enumerate(posts):
        post.display_number = start_index - idx  # 핵심 라인

    return render(request, 'board/board.html', {
        'posts': posts
    })


@login_required
def write_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user.username
            post.save()
            return redirect('board:post_detail', post.id)
    else:
        form = PostForm()

    return render(request, 'board/write.html', {'form': form})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author.strip().lower() != request.user.username.strip().lower() and not request.user.is_superuser:
        return redirect('board:board') 

    if post.upload:
        file_path = post.upload.path
        if os.path.exists(file_path):
            os.remove(file_path)

    post.delete()

    return redirect('board:board')

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # 작성자만 수정 가능
    if post.author != request.user.username:
        return redirect('board:board')  # 권한이 없을 경우 게시판으로 리디렉션

    # 게시글 수정 폼 불러오기
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()  # 폼 저장
            return redirect('board:board')  # 게시글 목록으로 리디렉션
    else:
        form = PostForm(instance=post)

    return render(request, 'board/edit_post.html', {'form': form})
