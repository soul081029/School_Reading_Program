from django import forms
from django.contrib.auth import authenticate

from .models import User


class SignupForm(forms.ModelForm):
    """회원가입 입력값과 검증을 처리하는 폼입니다."""

    password = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput(attrs={'placeholder': '비밀번호'}),
    )
    password_confirm = forms.CharField(
        label='비밀번호 확인',
        widget=forms.PasswordInput(attrs={'placeholder': '비밀번호 확인'}),
    )

    class Meta:
        model = User
        fields = ['student_id', 'password', 'password_confirm']
        labels = {
            'student_id': '학번',
        }
        widgets = {
            'student_id': forms.TextInput(
                attrs={
                    'placeholder': '5자리 학번',
                    'maxlength': '5',
                    'inputmode': 'numeric',
                }
            ),
        }

    def clean_student_id(self):
        """학번이 숫자 5자리이며 중복되지 않는지 검사합니다."""
        student_id = self.cleaned_data.get('student_id', '').strip()

        if not student_id.isdigit():
            raise forms.ValidationError('학번은 숫자만 입력할 수 있습니다.')

        if len(student_id) != 5:
            raise forms.ValidationError('학번은 정확히 5자리여야 합니다.')

        if User.objects.filter(student_id=student_id).exists():
            raise forms.ValidationError('이미 가입된 학번입니다.')

        return student_id

    def clean(self):
        """비밀번호와 비밀번호 확인 값이 일치하는지 검사합니다."""
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', '비밀번호가 일치하지 않습니다.')

        return cleaned_data

    def save(self, commit=True):
        """비밀번호를 평문이 아닌 해시 값으로 저장합니다."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()

        return user


class LoginForm(forms.Form):
    """학번과 비밀번호로 로그인 인증을 처리하는 폼입니다."""

    student_id = forms.CharField(
        label='학번',
        max_length=5,
        widget=forms.TextInput(
            attrs={
                'placeholder': '5자리 학번',
                'maxlength': '5',
                'inputmode': 'numeric',
            }
        ),
    )
    password = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput(attrs={'placeholder': '비밀번호'}),
    )

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.user = None

    def clean(self):
        """입력된 학번과 비밀번호로 사용자를 인증합니다."""
        cleaned_data = super().clean()
        student_id = cleaned_data.get('student_id')
        password = cleaned_data.get('password')

        if student_id and password:
            self.user = authenticate(
                self.request,
                username=student_id,
                password=password,
            )

            if self.user is None:
                raise forms.ValidationError('학번 또는 비밀번호가 올바르지 않습니다.')

        return cleaned_data

    def get_user(self):
        """인증에 성공한 사용자 객체를 반환합니다."""
        return self.user
