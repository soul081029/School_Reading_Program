from django.contrib import admin

from .models import Comment, Recommendation


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    """관리자 페이지에서 추천글을 관리합니다."""

    list_display = ('writer_name', 'book_title', 'created_at', 'is_anonymous')
    list_filter = ('is_anonymous', 'created_at')
    search_fields = ('book_title', 'book_author', 'writer_name')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """관리자 페이지에서 댓글을 관리합니다."""

    list_display = ('recommendation', 'writer_name', 'created_at')
    search_fields = ('writer_name', 'comment')
    readonly_fields = ('created_at',)
    ordering = ('created_at',)
