from django.urls import path
from muze import views
from django.contrib.auth import views as auth_views

app_name='muze'
urlpatterns = [
    path('', views.main, name='main'),
    path('concert/', views.ticket_list, name='ticket_list'),
    path('concert/create/', views.concert_create, name='concert_create'),
    path('tickets/<int:concert_id>/', views.ticket_sebu, name='ticket_sebu'),
    path('concert/<int:concert_id>/like/', views.like_concert, name='like_concert'),
    path('login/', auth_views.LoginView.as_view(template_name='muze/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('booking/<int:concert_id>/', views.ticket_booking, name='ticket_booking'),
    path('delete_review/<int:review_id>/', views.delete_review, name='delete_review'),
]
