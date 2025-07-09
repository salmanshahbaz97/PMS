from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import User, Coach, Player, Goal, ProcessGoal


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User Admin with role-based fields"""
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'date_of_birth', 'profile_picture')}),
        ('Role & Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'first_name', 'last_name'),
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('coach_profile', 'player_profile')


@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    """Coach Admin with enhanced display"""
    list_display = ('user', 'specialization', 'experience_years', 'hire_date', 'players_count', 'user_email')
    list_filter = ('specialization', 'experience_years', 'hire_date')
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'specialization')
    ordering = ('user__first_name', 'user__last_name')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Professional Information', {
            'fields': ('specialization', 'experience_years', 'bio')
        }),
        ('Employment', {
            'fields': ('hire_date',)
        }),
    )
    
    readonly_fields = ('hire_date',)
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'
    
    def players_count(self, obj):
        count = obj.get_players_count()
        return format_html('<span style="color: green; font-weight: bold;">{}</span>', count)
    players_count.short_description = 'Players Count'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    """Player Admin with enhanced display and coach assignment"""
    list_display = ('user', 'jersey_number', 'position', 'coach', 'is_active', 'join_date', 'age_display')
    list_filter = ('position', 'is_active', 'join_date', 'coach')
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'position', 'jersey_number')
    ordering = ('user__first_name', 'user__last_name')
    list_editable = ('coach', 'is_active')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Player Information', {
            'fields': ('position', 'jersey_number', 'height', 'weight')
        }),
        ('Assignment', {
            'fields': ('coach', 'is_active')
        }),
        ('Timeline', {
            'fields': ('join_date',)
        }),
    )
    
    readonly_fields = ('join_date',)
    
    def age_display(self, obj):
        age = obj.get_age()
        if age:
            return f"{age} years"
        return "N/A"
    age_display.short_description = 'Age'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'coach__user')
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "coach":
            kwargs["queryset"] = Coach.objects.select_related('user').order_by('user__first_name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    """Goal Admin with enhanced display and filtering"""
    list_display = ('name', 'player', 'coach', 'area', 'timeframe', 'progress', 'target_date', 'is_overdue_display', 'get_process_goals_count')
    list_filter = ('area', 'timeframe', 'progress', 'created_at', 'coach')
    search_fields = ('name', 'player__user__first_name', 'player__user__last_name', 'coach__user__first_name')
    ordering = ('-created_at',)
    list_editable = ('progress',)
    
    fieldsets = (
        ('Goal Information', {
            'fields': ('name', 'description', 'area', 'timeframe', 'target_date')
        }),
        ('Assignment', {
            'fields': ('player', 'coach')
        }),
        ('Progress Tracking', {
            'fields': ('progress', 'notes')
        }),
        ('Timeline', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def is_overdue_display(self, obj):
        if obj.is_overdue():
            return format_html('<span style="color: red; font-weight: bold;">Overdue</span>')
        return format_html('<span style="color: green;">On Track</span>')
    is_overdue_display.short_description = 'Status'
    
    def get_process_goals_count(self, obj):
        return obj.get_process_goals_count()
    get_process_goals_count.short_description = 'Process Goals'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('player__user', 'coach__user')
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "player":
            kwargs["queryset"] = Player.objects.select_related('user').filter(is_active=True).order_by('user__first_name')
        elif db_field.name == "coach":
            kwargs["queryset"] = Coach.objects.select_related('user').order_by('user__first_name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(ProcessGoal)
class ProcessGoalAdmin(admin.ModelAdmin):
    """Process Goal Admin with enhanced display and filtering"""
    list_display = ('name', 'main_goal', 'progress', 'target_date', 'order', 'is_overdue_display')
    list_filter = ('progress', 'created_at', 'main_goal__coach', 'main_goal__player')
    search_fields = ('name', 'main_goal__name', 'main_goal__player__user__first_name', 'main_goal__player__user__last_name')
    ordering = ('main_goal', 'order', 'created_at')
    list_editable = ('progress', 'order')
    
    fieldsets = (
        ('Process Goal Information', {
            'fields': ('name', 'main_goal', 'description')
        }),
        ('Goal Details', {
            'fields': ('progress', 'target_date', 'order')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
        ('Timeline', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def is_overdue_display(self, obj):
        if obj.is_overdue():
            return format_html('<span style="color: red; font-weight: bold;">Overdue</span>')
        return format_html('<span style="color: green;">On Track</span>')
    is_overdue_display.short_description = 'Status'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('main_goal__player__user', 'main_goal__coach__user')
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "main_goal":
            kwargs["queryset"] = Goal.objects.select_related('player__user', 'coach__user').order_by('name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# Customize admin site
admin.site.site_header = "Player Management System"
admin.site.site_title = "PMS Admin"
admin.site.index_title = "Welcome to Player Management System"
