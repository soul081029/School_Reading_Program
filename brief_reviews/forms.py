from django import forms

from .models import BookQuote


class BookQuoteForm(forms.ModelForm):
    """책 한 줄 작성과 수정을 처리하는 폼입니다."""

    class Meta:
        model = BookQuote
        fields = ['book_title', 'post_text']
        labels = {
            'book_title': '책 제목',
            'post_text': '책 한 줄 내용',
        }
        widgets = {
            'book_title': forms.TextInput(
                attrs={
                    'placeholder': '책 제목을 입력하세요.',
                    'maxlength': '100',
                }
            ),
            'post_text': forms.Textarea(
                attrs={
                    'placeholder': '인상 깊었던 문장이나 감상을 적어주세요.',
                    'rows': 4,
                }
            ),
        }

    def clean_book_title(self):
        """책 제목이 비어 있지 않은지 검사합니다."""
        book_title = self.cleaned_data.get('book_title', '').strip()

        if not book_title:
            raise forms.ValidationError('책 제목을 입력하세요.')

        if len(book_title) > 100:
            raise forms.ValidationError('책 제목은 100자 이내로 입력하세요.')

        return book_title

    def clean_post_text(self):
        """책 한 줄 내용이 비어 있지 않은지 검사합니다."""
        post_text = self.cleaned_data.get('post_text', '').strip()

        if not post_text:
            raise forms.ValidationError('책 한 줄 내용을 입력하세요.')

        return post_text
