from django.urls import path
from django.shortcuts import redirect
from . import views

app_name = 'core'

urlpatterns = [
    # Root redirect to login
    path('', lambda request: redirect('core:login'), name='home'),
    
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Profile
    path('profile/', views.profile_view, name='profile'),
    
    # Coach views (Admin only)
    path('coaches/', views.CoachListView.as_view(), name='coach_list'),
    
    # Player views
    path('players/', views.PlayerListView.as_view(), name='player_list'),
    path('players/<int:pk>/', views.PlayerDetailView.as_view(), name='player_detail'),
    
    # Goal views
    path('goals/', views.GoalListView.as_view(), name='goal_list'),
    path('goals/create/', views.GoalCreateView.as_view(), name='goal_create'),
    path('goals/<int:pk>/', views.GoalDetailView.as_view(), name='goal_detail'),
    path('goals/<int:pk>/edit/', views.GoalUpdateView.as_view(), name='goal_update'),
    path('goals/<int:pk>/progress/', views.goal_progress_update, name='goal_progress_update'),
    
    # Process Goal views
    path('goals/<int:goal_id>/process-goals/', views.ProcessGoalListView.as_view(), name='process_goal_list'),
    path('goals/<int:goal_id>/process-goals/create/', views.ProcessGoalCreateView.as_view(), name='process_goal_create'),
    path('process-goals/<int:pk>/edit/', views.ProcessGoalUpdateView.as_view(), name='process_goal_update'),
    path('process-goals/<int:pk>/progress/', views.process_goal_progress_update, name='process_goal_progress_update'),
] 