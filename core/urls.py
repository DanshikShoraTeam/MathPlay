from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/stats/', views.full_stats, name='full_stats'),
    path('dashboard/students/', views.student_list, name='student_list'),
    path('games/create/', views.game_create_type, name='game_create_type'),
    path('games/create/<str:gtype>/', views.game_create_form, name='game_create_form'),
    path('games/<int:pk>/', views.game_detail, name='game_detail'),
    path('games/<int:pk>/edit/', views.game_edit, name='game_edit'),
    path('games/<int:pk>/stats/', views.game_stats, name='game_stats'),
    path('games/<int:pk>/publish/', views.game_quick_publish, name='game_quick_publish'),
    path('games/<int:pk>/unpublish/', views.game_unpublish, name='game_unpublish'),
    path('games/<int:pk>/delete/', views.game_delete, name='game_delete'),
    path('play/<code>/', views.play_entry, name='play_entry'),
    path('play/<code>/game/', views.play_game, name='play_game'),
    path('play/<code>/result/<int:session_id>/', views.play_result, name='play_result'),
]
