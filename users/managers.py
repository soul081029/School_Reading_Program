from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """학번 기반 사용자 생성을 담당하는 매니저입니다."""

    def create_user(self, student_id, password=None, **extra_fields):
        """일반 학생 계정을 생성합니다."""
        if not student_id:
            raise ValueError('학번은 반드시 입력해야 합니다.')

        student_id = str(student_id)
        user = self.model(student_id=student_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, student_id, password=None, **extra_fields):
        """관리자 페이지에 접근할 수 있는 최고 관리자 계정을 생성합니다."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('관리자 계정은 is_staff=True 이어야 합니다.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('관리자 계정은 is_superuser=True 이어야 합니다.')

        return self.create_user(student_id, password, **extra_fields)
