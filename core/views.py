from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth import logout
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import JsonResponse
from .models import User, Coach, Player, Goal, ProcessGoal


def login_view(request):
    """Custom login view with role-based redirect"""
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        from django.contrib.auth import authenticate, login
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name()}!')
            return redirect('core:dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'core/login.html')


@login_required
def dashboard(request):
    """Role-based dashboard"""
    user = request.user
    
    if user.is_admin():
        return admin_dashboard(request)
    elif user.is_coach():
        return coach_dashboard(request)
    elif user.is_player():
        return player_dashboard(request)
    else:
        messages.error(request, 'Invalid user role.')
        return redirect('core:login')


def admin_dashboard(request):
    """Admin dashboard with overview of all users"""
    context = {
        'total_users': User.objects.count(),
        'total_coaches': Coach.objects.count(),
        'total_players': Player.objects.count(),
        'active_players': Player.objects.filter(is_active=True).count(),
        'recent_players': Player.objects.select_related('user', 'coach__user').order_by('-join_date')[:5],
        'recent_coaches': Coach.objects.select_related('user').order_by('-hire_date')[:5],
    }
    return render(request, 'core/admin_dashboard.html', context)


def coach_dashboard(request):
    """Coach dashboard with assigned players"""
    try:
        coach = request.user.coach_profile
        context = {
            'coach': coach,
            'players': coach.players.select_related('user').filter(is_active=True),
            'total_players': coach.get_players_count(),
        }
        return render(request, 'core/coach_dashboard.html', context)
    except Coach.DoesNotExist:
        messages.error(request, 'Coach profile not found. Please contact administrator.')
        return redirect('core:login')


def player_dashboard(request):
    """Player dashboard with personal information"""
    try:
        player = request.user.player_profile
        context = {
            'player': player,
            'coach': player.coach,
        }
        return render(request, 'core/player_dashboard.html', context)
    except Player.DoesNotExist:
        messages.error(request, 'Player profile not found. Please contact administrator.')
        return redirect('core:login')


class AdminRequiredMixin(UserPassesTestMixin):
    """Mixin to ensure only admins can access"""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin()


class CoachRequiredMixin(UserPassesTestMixin):
    """Mixin to ensure only coaches can access"""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_coach()


class PlayerRequiredMixin(UserPassesTestMixin):
    """Mixin to ensure only players can access"""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_player()


class CoachListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    """List all coaches for admin"""
    model = Coach
    template_name = 'core/coach_list.html'
    context_object_name = 'coaches'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Coach.objects.select_related('user').order_by('user__first_name')
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(user__email__icontains=search) |
                Q(specialization__icontains=search)
            )
        return queryset


class PlayerListView(LoginRequiredMixin, ListView):
    """List players - filtered by role"""
    model = Player
    template_name = 'core/player_list.html'
    context_object_name = 'players'
    paginate_by = 10
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_admin():
            # Admin sees all players
            queryset = Player.objects.select_related('user', 'coach__user')
        elif user.is_coach():
            # Coach sees only assigned players
            try:
                coach = user.coach_profile
                queryset = coach.players.select_related('user')
            except Coach.DoesNotExist:
                queryset = Player.objects.none()
        else:
            # Players see only themselves
            queryset = Player.objects.filter(user=user)
        
        # Apply search filter
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(position__icontains=search) |
                Q(jersey_number__icontains=search)
            )
        
        return queryset.order_by('user__first_name', 'user__last_name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_role'] = self.request.user.role
        return context


class PlayerDetailView(LoginRequiredMixin, DetailView):
    """Player detail view with role-based access"""
    model = Player
    template_name = 'core/player_detail.html'
    context_object_name = 'player'
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_admin():
            # Admin can see all players
            return Player.objects.select_related('user', 'coach__user')
        elif user.is_coach():
            # Coach can see only assigned players
            try:
                coach = user.coach_profile
                return coach.players.select_related('user')
            except Coach.DoesNotExist:
                return Player.objects.none()
        else:
            # Players can see only themselves
            return Player.objects.filter(user=user).select_related('user', 'coach__user')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_role'] = self.request.user.role
        return context


@login_required
def profile_view(request):
    """User profile view"""
    user = request.user
    
    if user.is_coach():
        try:
            profile = user.coach_profile
            template = 'core/coach_profile.html'
        except Coach.DoesNotExist:
            messages.error(request, 'Coach profile not found. Please contact administrator.')
            return redirect('core:dashboard')
    elif user.is_player():
        try:
            profile = user.player_profile
            template = 'core/player_profile.html'
        except Player.DoesNotExist:
            messages.error(request, 'Player profile not found. Please contact administrator.')
            return redirect('core:dashboard')
    else:
        # Admin profile
        profile = user
        template = 'core/admin_profile.html'
    
    context = {
        'profile': profile,
        'user_role': user.role,
    }
    return render(request, template, context)


@login_required
def logout_view(request):
    """Custom logout view"""
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('core:login')


# Goal-related views
class GoalListView(LoginRequiredMixin, ListView):
    """List goals - filtered by role"""
    model = Goal
    template_name = 'core/goal_list.html'
    context_object_name = 'goals'
    paginate_by = 10
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_admin():
            # Admin sees all goals
            queryset = Goal.objects.select_related('player__user', 'coach__user')
        elif user.is_coach():
            # Coach sees goals they assigned
            try:
                coach = user.coach_profile
                queryset = coach.assigned_goals.select_related('player__user')
            except Coach.DoesNotExist:
                queryset = Goal.objects.none()
        else:
            # Players see only their own goals
            try:
                player = user.player_profile
                queryset = player.goals.select_related('coach__user')
            except Player.DoesNotExist:
                queryset = Goal.objects.none()
        
        # Apply search filter
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(player__user__first_name__icontains=search) |
                Q(player__user__last_name__icontains=search) |
                Q(area__icontains=search)
            )
        
        # Apply area filter
        area = self.request.GET.get('area')
        if area:
            queryset = queryset.filter(area=area)
        
        # Apply progress filter
        progress = self.request.GET.get('progress')
        if progress:
            queryset = queryset.filter(progress=progress)
        
        # Apply timeframe filter
        timeframe = self.request.GET.get('timeframe')
        if timeframe:
            queryset = queryset.filter(timeframe=timeframe)
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_role'] = self.request.user.role
        return context


class GoalCreateView(LoginRequiredMixin, CoachRequiredMixin, CreateView):
    """Create new goal - coaches only"""
    model = Goal
    template_name = 'core/goal_form.html'
    fields = ['name', 'player', 'area', 'timeframe', 'description', 'target_date']
    success_url = reverse_lazy('core:goal_list')
    
    def form_valid(self, form):
        form.instance.coach = self.request.user.coach_profile
        messages.success(self.request, 'Goal created successfully!')
        return super().form_valid(form)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Only show players assigned to this coach
        try:
            coach = self.request.user.coach_profile
            form.fields['player'].queryset = coach.players.filter(is_active=True)
        except Coach.DoesNotExist:
            form.fields['player'].queryset = Player.objects.none()
        return form


class GoalUpdateView(LoginRequiredMixin, UpdateView):
    """Update goal - coaches can update all fields, players can update progress only"""
    model = Goal
    template_name = 'core/goal_form.html'
    fields = ['name', 'player', 'area', 'timeframe', 'description', 'target_date', 'notes', 'progress']
    
    def get_fields(self):
        user = self.request.user
        if user.is_coach():
            return ['name', 'player', 'area', 'timeframe', 'description', 'target_date', 'notes']
        else:
            return ['progress', 'notes']
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_admin():
            return Goal.objects.all()
        elif user.is_coach():
            try:
                coach = user.coach_profile
                return coach.assigned_goals.all()
            except Coach.DoesNotExist:
                return Goal.objects.none()
        else:
            try:
                player = user.player_profile
                return player.goals.all()
            except Player.DoesNotExist:
                return Goal.objects.none()
    
    def get_success_url(self):
        messages.success(self.request, 'Goal updated successfully!')
        return reverse_lazy('core:goal_list')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        
        if user.is_coach():
            # Only show players assigned to this coach
            try:
                coach = user.coach_profile
                form.fields['player'].queryset = coach.players.filter(is_active=True)
            except Coach.DoesNotExist:
                form.fields['player'].queryset = Player.objects.none()
        
        return form


class GoalDetailView(LoginRequiredMixin, DetailView):
    """Goal detail view with role-based access"""
    model = Goal
    template_name = 'core/goal_detail.html'
    context_object_name = 'goal'
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_admin():
            return Goal.objects.select_related('player__user', 'coach__user')
        elif user.is_coach():
            try:
                coach = user.coach_profile
                return coach.assigned_goals.select_related('player__user')
            except Coach.DoesNotExist:
                return Goal.objects.none()
        else:
            try:
                player = user.player_profile
                return player.goals.select_related('coach__user')
            except Player.DoesNotExist:
                return Goal.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_role'] = self.request.user.role
        return context


@login_required
def goal_progress_update(request, pk):
    """AJAX endpoint for updating goal progress"""
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        goal = get_object_or_404(Goal, pk=pk)
        
        # Check if user has permission to update this goal
        user = request.user
        can_update = False
        error_message = None
        
        if user.is_admin():
            can_update = True
        elif user.is_coach():
            try:
                can_update = goal.coach == user.coach_profile
            except Coach.DoesNotExist:
                error_message = 'Coach profile not found'
                can_update = False
        else:
            try:
                can_update = goal.player == user.player_profile
            except Player.DoesNotExist:
                error_message = 'Player profile not found'
                can_update = False
        
        if not can_update:
            return JsonResponse({
                'error': error_message or 'Permission denied',
                'user_role': user.role,
                'goal_player_id': goal.player.id if goal.player else None,
                'user_profile_id': user.player_profile.id if hasattr(user, 'player_profile') else None
            }, status=403)
        
        progress = request.POST.get('progress')
        notes = request.POST.get('notes', '')
        
        if progress in dict(Goal.PROGRESS_CHOICES):
            goal.progress = progress
            if notes:
                goal.notes = notes
            goal.save()
            
            return JsonResponse({
                'success': True,
                'progress': progress,
                'progress_percentage': goal.get_progress_percentage(),
                'is_overdue': goal.is_overdue()
            })
        
        return JsonResponse({'error': 'Invalid progress value'}, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


# Process Goal views
class ProcessGoalListView(LoginRequiredMixin, ListView):
    """List process goals for a specific main goal"""
    model = ProcessGoal
    template_name = 'core/process_goal_list.html'
    context_object_name = 'process_goals'
    paginate_by = 10
    
    def get_queryset(self):
        goal_id = self.kwargs.get('goal_id')
        goal = get_object_or_404(Goal, pk=goal_id)
        
        # Check permissions
        user = self.request.user
        if user.is_admin():
            pass  # Admin can see all
        elif user.is_coach():
            try:
                if goal.coach != user.coach_profile:
                    return ProcessGoal.objects.none()
            except Coach.DoesNotExist:
                return ProcessGoal.objects.none()
        else:
            try:
                if goal.player != user.player_profile:
                    return ProcessGoal.objects.none()
            except Player.DoesNotExist:
                return ProcessGoal.objects.none()
        
        return goal.process_goals.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        goal_id = self.kwargs.get('goal_id')
        context['goal'] = get_object_or_404(Goal, pk=goal_id)
        context['user_role'] = self.request.user.role
        return context


class ProcessGoalCreateView(LoginRequiredMixin, CoachRequiredMixin, CreateView):
    """Create new process goal - coaches only"""
    model = ProcessGoal
    template_name = 'core/process_goal_form.html'
    fields = ['name', 'description', 'target_date', 'order', 'progress']
    success_url = reverse_lazy('core:goal_list')
    
    def form_valid(self, form):
        goal_id = self.kwargs.get('goal_id')
        goal = get_object_or_404(Goal, pk=goal_id)
        
        # Check if coach owns this goal
        try:
            if goal.coach != self.request.user.coach_profile:
                messages.error(self.request, 'You can only add process goals to your own goals.')
                return self.form_invalid(form)
        except Coach.DoesNotExist:
            messages.error(self.request, 'Coach profile not found. Please contact administrator.')
            return self.form_invalid(form)
        
        form.instance.main_goal = goal
        # Set default progress to not_started for new process goals
        if not form.instance.progress:
            form.instance.progress = 'not_started'
        
        messages.success(self.request, 'Process goal created successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        goal_id = self.kwargs.get('goal_id')
        return reverse_lazy('core:process_goal_list', kwargs={'goal_id': goal_id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        goal_id = self.kwargs.get('goal_id')
        context['goal'] = get_object_or_404(Goal, pk=goal_id)
        return context


class ProcessGoalUpdateView(LoginRequiredMixin, UpdateView):
    """Update process goal - coaches can update all fields, players can update progress only"""
    model = ProcessGoal
    template_name = 'core/process_goal_form.html'
    fields = ['name', 'description', 'target_date', 'order', 'progress', 'notes']
    
    def get_fields(self):
        user = self.request.user
        if user.is_coach():
            return ['name', 'description', 'target_date', 'order']
        else:
            return ['progress', 'notes']
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_admin():
            return ProcessGoal.objects.select_related('main_goal__player__user', 'main_goal__coach__user')
        elif user.is_coach():
            try:
                coach = user.coach_profile
                return ProcessGoal.objects.filter(main_goal__coach=coach).select_related('main_goal__player__user')
            except Coach.DoesNotExist:
                return ProcessGoal.objects.none()
        else:
            try:
                player = user.player_profile
                return ProcessGoal.objects.filter(main_goal__player=player).select_related('main_goal__coach__user')
            except Player.DoesNotExist:
                return ProcessGoal.objects.none()
    
    def get_success_url(self):
        messages.success(self.request, 'Process goal updated successfully!')
        return reverse_lazy('core:process_goal_list', kwargs={'goal_id': self.object.main_goal.id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['goal'] = self.object.main_goal
        return context


@login_required
def process_goal_progress_update(request, pk):
    """AJAX endpoint for updating process goal progress"""
    print(f"Process goal progress update called for pk: {pk}")
    print(f"Request method: {request.method}")
    print(f"Request headers: {request.headers}")
    
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        process_goal = get_object_or_404(ProcessGoal, pk=pk)
        print(f"Found process goal: {process_goal}")
        
        # Check if user has permission to update this process goal
        user = request.user
        can_update = False
        error_message = None
        
        if user.is_admin():
            can_update = True
        elif user.is_coach():
            try:
                can_update = process_goal.main_goal.coach == user.coach_profile
            except Coach.DoesNotExist:
                error_message = 'Coach profile not found'
                can_update = False
        else:
            try:
                can_update = process_goal.main_goal.player == user.player_profile
            except Player.DoesNotExist:
                error_message = 'Player profile not found'
                can_update = False
        
        if not can_update:
            return JsonResponse({
                'error': error_message or 'Permission denied',
                'user_role': user.role,
            }, status=403)
        
        progress = request.POST.get('progress')
        notes = request.POST.get('notes', '')
        
        if progress in dict(ProcessGoal.PROGRESS_CHOICES):
            process_goal.progress = progress
            if notes:
                process_goal.notes = notes
            process_goal.save()
            
            # Check if main goal should be auto-completed
            main_goal = process_goal.main_goal
            if main_goal.should_auto_complete():
                main_goal.progress = 'completed'
                main_goal.save()
            
            return JsonResponse({
                'success': True,
                'progress': progress,
                'progress_percentage': process_goal.get_progress_percentage(),
                'is_overdue': process_goal.is_overdue(),
                'main_goal_completed': main_goal.progress == 'completed'
            })
        
        return JsonResponse({'error': 'Invalid progress value'}, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)
