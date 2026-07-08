from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BookQuoteForm
from .models import BookQuote


def _can_manage_quote(user, quote):
    """작성자 본인 또는 관리자만 수정과 삭제를 허용합니다."""
    return user == quote.author or user.is_staff or user.is_superuser


def quote_list(request):
    """책 한 줄 목록을 보여줍니다."""
    quotes = BookQuote.objects.select_related('author').all()
    return render(request, 'brief_reviews/list.html', {'quotes': quotes})


@login_required
def quote_create(request):
    """로그인한 학생의 책 한 줄 작성을 처리합니다."""
    if request.method == 'POST':
        form = BookQuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.author = request.user
            quote.save()
            return redirect('quote_list')
    else:
        form = BookQuoteForm()

    return render(request, 'brief_reviews/create.html', {'form': form})


@login_required
def quote_update(request, id):
    """작성자 본인 또는 관리자의 책 한 줄 수정을 처리합니다."""
    quote = get_object_or_404(BookQuote, id=id)

    if not _can_manage_quote(request.user, quote):
        raise PermissionDenied

    if request.method == 'POST':
        form = BookQuoteForm(request.POST, instance=quote)
        if form.is_valid():
            quote = form.save()
            return redirect('quote_list')
    else:
        form = BookQuoteForm(instance=quote)

    return render(request, 'brief_reviews/edit.html', {'form': form, 'quote': quote})


@login_required
def quote_delete(request, id):
    """작성자 본인 또는 관리자의 책 한 줄 삭제를 처리합니다."""
    quote = get_object_or_404(BookQuote, id=id)

    if not _can_manage_quote(request.user, quote):
        raise PermissionDenied

    if request.method == 'POST':
        quote.delete()
        return redirect('quote_list')

    return render(request, 'brief_reviews/delete.html', {'quote': quote})
