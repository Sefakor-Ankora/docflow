from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create_memo/', views.create_memo, name='create_memo'),
    path('leave_request/', views.leave_request, name='leave_request'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    #path('logout/', views.user_logout, name='logout'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('memo_list/', views.memo_list, name='memo_list'),
    path('memo_detail/<int:memo_id>/', views.memo_detail, name='memo_detail'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='docflow/password_reset.html'), name='password_reset'),
    path('password_reset_complete/', auth_views.PasswordResetView.as_view(template_name='docflow/password_reset_complete.html'), name='password_reset_complete'),
    path('password_reset_confirm/', auth_views.PasswordResetView.as_view(template_name='docflow/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_done/', auth_views.PasswordResetView.as_view(template_name='docflow/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='docflow/password_reset_complete.html'), name='password_reset_complete'),
    # Add other URLs as needed
]
