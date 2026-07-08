from django import forms

from .models import Comment, Recommendation


class RecommendationForm(forms.ModelForm):
    """추천글 작성과 수정을 처리하는 폼입니다."""

    class Meta:
        model = Recommendation
        fields = ['is_anonymous', 'book_title', 'book_author', 'post_text']
        labels = {
            'is_anonymous': '익명으로 작성',
            'book_title': '책 제목',
            'book_author': '저자',
            'post_text': '추천 이유',
        }
        widgets = {
            'is_anonymous': forms.CheckboxInput(),
            'book_title': forms.TextInput(
                attrs={
                    'placeholder': '책 제목을 입력하세요.',
                    'maxlength': '100',
                }
            ),
            'book_author': forms.TextInput(
                attrs={
                    'placeholder': '저자를 입력하세요.',
                    'maxlength': '50',
                }
            ),
            'post_text': forms.Textarea(
                attrs={
                    'placeholder': '이 책을 추천하는 이유를 적어 주세요.',
                    'rows': 8,
                }
            ),
        }

    def clean_book_title(self):
        """책 제목이 비어 있지 않고 100자를 넘지 않는지 검사합니다."""
        book_title = self.cleaned_data.get('book_title', '').strip()

        if not book_title:
            raise forms.ValidationError('책 제목을 입력하세요.')

        if len(book_title) > 100:
            raise forms.ValidationError('책 제목은 100자 이내로 입력하세요.')

        return book_title

    def clean_book_author(self):
        """저자명이 비어 있지 않고 50자를 넘지 않는지 검사합니다."""
        book_author = self.cleaned_data.get('book_author', '').strip()

        if not book_author:
            raise forms.ValidationError('저자를 입력하세요.')

        if len(book_author) > 50:
            raise forms.ValidationError('저자는 50자 이내로 입력하세요.')

        return book_author

    def clean_post_text(self):
        """추천 이유가 비어 있지 않은지 검사합니다."""
        post_text = self.cleaned_data.get('post_text', '').strip()

        if not post_text:
            raise forms.ValidationError('추천 이유를 입력하세요.')

        return post_text


class CommentForm(forms.ModelForm):
    """댓글 작성을 처리하는 폼입니다."""

    class Meta:
        model = Comment
        fields = ['is_anonymous', 'comment']
        labels = {
            'is_anonymous': '익명으로 작성',
            'comment': '댓글',
        }
        widgets = {
            'is_anonymous': forms.CheckboxInput(),
            'comment': forms.Textarea(
                attrs={
                    'placeholder': '댓글을 입력하세요.',
                    'rows': 4,
                }
            ),
        }

    def clean_comment(self):
        """댓글 내용이 비어 있지 않은지 검사합니다."""
        comment = self.cleaned_data.get('comment', '').strip()

        if not comment:
            raise forms.ValidationError('댓글을 입력하세요.')

        return comment
