from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from .models import Concert, UserProfile, Review
from .forms import ConcertForm, UserForm, ReviewForm
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.contrib import messages
import random, calendar
from .models import Concert, Review
from django.contrib.auth.decorators import login_required
from board.models import Post

# Create your views here.

from django.shortcuts import render
from .models import Concert

def main(request):
    all_concerts = list(Concert.objects.all())
    random_concerts = random.sample(all_concerts, 4) if len(all_concerts) >= 4 else all_concerts
    top_concerts = Concert.objects.order_by('-likes')[:3]

    latest_reviews = list(
        Review.objects.select_related('concert')
        .order_by('-created_at')[:4]
    )

    latest_posts = Post.objects.order_by('-created_at')[:10]

    return render(request, 'muze/main.html', {
        'concerts': random_concerts,
        'top_concerts': top_concerts,
        'latest_reviews': latest_reviews,
	'latest_posts': latest_posts,
    })


def ticket_list(request):
    ranking_concerts = Concert.objects.order_by('-likes')[:3]
    all_concerts = Concert.objects.all().order_by('-id')
    return render(request, 'muze/ticket_list.html', {
        'ranking_concerts': ranking_concerts,
	'all_concerts': all_concerts,
    })


def ticket_sebu(request, concert_id):
    concert = get_object_or_404(Concert, id=concert_id)
    delivery_date = concert.date - timedelta(days=14)

#달력 구문
    year = concert.date.year
    month = concert.date.month
    concert_day = concert.date.day

    first_weekday, last_day = calendar.monthrange(year, month)

    calendar_matrix = []
    week = [0] * first_weekday  # 빈 칸 채우기

    for day in range(1, last_day + 1):
        week.append(day)
        if len(week) == 7:
            calendar_matrix.append(week)
            week = []

    if week:
        while len(week) < 7:
            week.append(0)
        calendar_matrix.append(week)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.concert = concert
            review.user = request.user
            review.nickname = request.user.username
            review.save()
            return redirect('muze:ticket_sebu', concert_id=concert.id)
    else:
        form = ReviewForm()
##


    reviews = concert.reviews.all().order_by('-created_at')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.concert = concert
            review.save()
            return redirect('muze:ticket_sebu', concert_id=concert.id)  # 새로고침
    else:
        form = ReviewForm()

    context = {
        'concert': concert,
        'delivery_date': delivery_date,
        'form': form,
        'reviews': reviews,
	'calendar_matrix': calendar_matrix,  #
	'concert_day': concert_day,          # 
    }

    return render(request, 'muze/ticket_sebu.html', context)

def concert_create(request):
    if request.method == 'POST':
        form = ConcertForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('muze:ticket_list')  # 저장 후 리스트로 이동
    else:
        form = ConcertForm()
    return render(request, 'muze/concert_create.html', {'form': form})

def like_concert(request, concert_id):
    concert = get_object_or_404(Concert, id=concert_id)
    concert.likes += 1
    concert.save()
    return JsonResponse({'likes': concert.likes})

def signup(request):
  if request.method == "POST":
    form = UserForm(request.POST)
    if form.is_valid():
      try:
        user = form.save()
        raw_password = form.cleaned_data.get('password1')
        name = request.POST.get('name')
        rrn = request.POST.get('rrn')
        UserProfile.objects.create(user=user, name=name, rrn=rrn)
        login(request, user)
        return redirect('/')
      except IntegrityError:
        if user:
          user.delete()  # 이미 저장된 user가 있으면 롤백
        messages.error(request, "이미 등록된 주민등록번호입니다.")
    else:
        messages.error(request, "입력한 정보에 오류가 있습니다.")
  else:
      form = UserForm()
  return render(request, 'muze/signup.html', {'form': form})


def ticket_booking(request, concert_id):
    # concert_id를 받아서 해당 콘서트를 가져옵니다.
    concert = get_object_or_404(Concert, id=concert_id)
    
    if request.method == 'POST':
        # 예매 처리 로직 (예: 결제 처리)
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        seats = request.POST['seats']
        # 예매 정보 저장 등
        pass
    
    return render(request, 'muze/ticket_booking.html', {'concert': concert})


# 메인에 리뷰 가져오는 메소드

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    # 로그인한 사용자가 리뷰의 작성자거나, 관리자인 경우 삭제 가능
    if review.user == request.user or request.user.is_staff:
        concert_id = review.concert.id  # 리뷰와 관련된 공연 ID를 가져옵니다.
        review.delete()
        return redirect('muze:ticket_sebu', concert_id=concert_id)  # 여기서 concert_id 사용
    else:
        return JsonResponse({'error': '삭제 권한이 없습니다.'}, status=403)
