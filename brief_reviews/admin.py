from django.contrib import admin

from .models import BookQuote


@admin.register(BookQuote)
class BookQuoteAdmin(admin.ModelAdmin):
    """관리자 페이지에서 책 한 줄을 관리합니다."""

    list_display = ('book_title', 'author', 'created_at')
    search_fields = ('book_title', 'post_text')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
