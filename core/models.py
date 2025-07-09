from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Custom User model with role-based authentication"""
    
    class Role(models.TextChoices):
        ADMIN = 'admin', _('Admin')
        COACH = 'coach', _('Coach')
        PLAYER = 'player', _('Player')
    
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.PLAYER,
        verbose_name=_('Role')
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True,
        verbose_name=_('Profile Picture')
    )
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"
    
    def is_admin(self):
        return self.role == self.Role.ADMIN
    
    def is_coach(self):
        return self.role == self.Role.COACH
    
    def is_player(self):
        return self.role == self.Role.PLAYER

    @property
    def is_player_prop(self):
        return self.is_player()

    @property
    def is_coach_prop(self):
        return self.is_coach()

    @property
    def is_admin_prop(self):
        return self.is_admin()


class Coach(models.Model):
    """Coach model linked to User"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='coach_profile',
        verbose_name=_('User')
    )
    specialization = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('Specialization')
    )
    experience_years = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Years of Experience')
    )
    bio = models.TextField(
        blank=True,
        verbose_name=_('Biography')
    )
    hire_date = models.DateField(
        auto_now_add=True,
        verbose_name=_('Hire Date')
    )
    
    class Meta:
        verbose_name = _('Coach')
        verbose_name_plural = _('Coaches')
    
    def __str__(self):
        return f"Coach {self.user.get_full_name()}"
    
    def get_players_count(self):
        return self.players.count()


class Player(models.Model):
    """Player model linked to User and Coach"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='player_profile',
        verbose_name=_('User')
    )
    coach = models.ForeignKey(
        Coach,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='players',
        verbose_name=_('Assigned Coach')
    )
    position = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_('Position')
    )
    jersey_number = models.PositiveIntegerField(
        blank=True,
        null=True,
        unique=True,
        verbose_name=_('Jersey Number')
    )
    height = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name=_('Height (cm)')
    )
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name=_('Weight (kg)')
    )
    join_date = models.DateField(
        auto_now_add=True,
        verbose_name=_('Join Date')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Active Status')
    )
    
    class Meta:
        verbose_name = _('Player')
        verbose_name_plural = _('Players')
        ordering = ['user__first_name', 'user__last_name']
    
    def __str__(self):
        return f"Player {self.user.get_full_name()} (#{self.jersey_number})"
    
    def get_full_name(self):
        return self.user.get_full_name()
    
    def get_age(self):
        if self.user.date_of_birth:
            from datetime import date
            today = date.today()
            return today.year - self.user.date_of_birth.year - (
                (today.month, today.day) < (self.user.date_of_birth.month, self.user.date_of_birth.day)
            )
        return None


class Goal(models.Model):
    """Goal model for players to track their progress"""
    
    PROGRESS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('good_progress', 'Good Progress'),
        ('excellent_progress', 'Excellent Progress'),
        ('completed', 'Completed'),
    ]
    
    TIMEFRAME_CHOICES = [
        ('short_term', 'Short Term'),
        ('medium_term', 'Medium Term'),
        ('long_term', 'Long Term'),
    ]
    
    AREA_CHOICES = [
        ('physical', 'Physical'),
        ('technical', 'Technical'),
        ('tactical', 'Tactical'),
        ('mental', 'Mental'),
    ]
    
    name = models.CharField(max_length=200, help_text="Goal name/description")
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='goals')
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE, related_name='assigned_goals')
    area = models.CharField(max_length=20, choices=AREA_CHOICES, default='technical')
    timeframe = models.CharField(max_length=20, choices=TIMEFRAME_CHOICES, default='medium_term')
    progress = models.CharField(max_length=20, choices=PROGRESS_CHOICES, default='not_started')
    description = models.TextField(blank=True, help_text="Detailed description of the goal")
    target_date = models.DateField(null=True, blank=True, help_text="Target completion date")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, help_text="Additional notes or comments")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Goal'
        verbose_name_plural = 'Goals'
    
    def __str__(self):
        return f"{self.name} - {self.player.user.get_full_name()}"
    
    def get_progress_percentage(self):
        """Calculate progress percentage based on status"""
        progress_map = {
            'not_started': 0,
            'in_progress': 25,
            'good_progress': 50,
            'excellent_progress': 75,
            'completed': 100,
        }
        return progress_map.get(self.progress, 0)
    
    def is_overdue(self):
        """Check if goal is overdue"""
        if self.target_date and self.progress != 'completed':
            from django.utils import timezone
            return self.target_date < timezone.now().date()
        return False
    
    def get_process_goals_count(self):
        """Get total number of process goals"""
        return self.process_goals.count()
    
    def get_completed_process_goals_count(self):
        """Get number of completed process goals"""
        return self.process_goals.filter(progress='completed').count()
    
    def get_completion_percentage(self):
        """Calculate completion percentage based on process goals"""
        total_process_goals = self.get_process_goals_count()
        if total_process_goals == 0:
            # If no process goals, use the old progress percentage
            return self.get_progress_percentage()
        
        completed_process_goals = self.get_completed_process_goals_count()
        return int((completed_process_goals / total_process_goals) * 100)
    
    def should_auto_complete(self):
        """Check if goal should be auto-completed based on process goals"""
        total_process_goals = self.get_process_goals_count()
        if total_process_goals == 0:
            return False
        
        completed_process_goals = self.get_completed_process_goals_count()
        return completed_process_goals == total_process_goals


class ProcessGoal(models.Model):
    """Process Goal model for sub-goals under main goals"""
    
    PROGRESS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('good_progress', 'Good Progress'),
        ('excellent_progress', 'Excellent Progress'),
        ('completed', 'Completed'),
    ]
    
    name = models.CharField(max_length=200, help_text="Process goal name/description")
    main_goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='process_goals')
    progress = models.CharField(max_length=20, choices=PROGRESS_CHOICES, default='not_started')
    description = models.TextField(blank=True, help_text="Detailed description of the process goal")
    target_date = models.DateField(null=True, blank=True, help_text="Target completion date")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, help_text="Additional notes or comments")
    order = models.PositiveIntegerField(default=0, help_text="Order of the process goal")
    
    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = 'Process Goal'
        verbose_name_plural = 'Process Goals'
    
    def __str__(self):
        return f"{self.name} - {self.main_goal.name}"
    
    def get_progress_percentage(self):
        """Calculate progress percentage based on status"""
        progress_map = {
            'not_started': 0,
            'in_progress': 25,
            'good_progress': 50,
            'excellent_progress': 75,
            'completed': 100,
        }
        return progress_map.get(self.progress, 0)
    
    def is_overdue(self):
        """Check if process goal is overdue"""
        if self.target_date and self.progress != 'completed':
            from django.utils import timezone
            return self.target_date < timezone.now().date()
        return False
