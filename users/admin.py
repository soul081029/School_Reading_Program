from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """관리자 페이지에서 학번 기반 사용자 모델을 관리합니다."""

    model = User
    list_display = ('student_id', 'is_staff', 'is_superuser', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('student_id',)
    ordering = ('student_id',)

    fieldsets = (
        (None, {'fields': ('student_id', 'password')}),
        ('권한', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('중요한 날짜', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('student_id', 'password1', 'password2', 'is_staff', 'is_superuser', 'is_active'),
            },
        ),
    )
