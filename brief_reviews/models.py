from django.conf import settings
from django.db import models


class BookQuote(models.Model):
    """학생이 공유하는 책 한 줄입니다."""

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='book_quotes',
        verbose_name='작성자',
    )
    book_title = models.CharField(max_length=100, verbose_name='책 제목')
    post_text = models.TextField(verbose_name='책 한 줄 내용')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        ordering = ['-created_at']
        verbose_name = '책 한 줄'
        verbose_name_plural = '책 한 줄'

    def __str__(self):
        return f'{self.book_title} - {self.author.student_id}'
