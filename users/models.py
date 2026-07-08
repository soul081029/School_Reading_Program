from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


class User(AbstractUser):
    """학번을 로그인 ID로 사용하는 학생 계정 모델입니다."""

    # 기본 username 필드는 사용하지 않습니다.
    username = None

    # 학생은 5자리 학번 하나로 식별됩니다.
    student_id = models.CharField(
        max_length=5,
        unique=True,
        verbose_name='학번',
        help_text='5자리 숫자 학번을 입력하세요.',
    )

    objects = UserManager()

    USERNAME_FIELD = 'student_id'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.student_id
