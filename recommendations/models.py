from django.conf import settings
from django.db import models


class Recommendation(models.Model):
    """학생이 작성한 책 추천글입니다."""

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recommendations',
        verbose_name='작성자',
    )
    is_anonymous = models.BooleanField(default=False, verbose_name='익명 여부')
    writer_name = models.CharField(max_length=20, verbose_name='작성자 표시')
    book_title = models.CharField(max_length=100, verbose_name='책 제목')
    book_author = models.CharField(max_length=50, verbose_name='저자')
    post_text = models.TextField(verbose_name='추천 이유')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        ordering = ['-created_at']
        verbose_name = '추천글'
        verbose_name_plural = '추천글'

    def __str__(self):
        return f'{self.book_title} - {self.writer_name}'


class Comment(models.Model):
    """추천글에 작성하는 댓글입니다."""

    recommendation = models.ForeignKey(
        Recommendation,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='추천글',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='작성자',
    )
    is_anonymous = models.BooleanField(default=False, verbose_name='익명 여부')
    writer_name = models.CharField(max_length=30, verbose_name='작성자 표시')
    comment = models.TextField(verbose_name='댓글')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성일')

    class Meta:
        ordering = ['created_at']
        verbose_name = '댓글'
        verbose_name_plural = '댓글'

    def __str__(self):
        return f'{self.writer_name} - {self.comment[:20]}'
