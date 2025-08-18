from django.urls import path
from . import views
from django.conf.urls.static import static

app_name = 'board'

urlpatterns = [
    path('', views.board_view, name='board'),
    path('write/', views.write_post, name='write'),
    path('<int:post_id>/', views.post_detail, name='post_detail'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('edit/<int:post_id>/', views.edit_post, name='edit_post'),
]
