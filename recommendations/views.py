from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import CommentForm, RecommendationForm
from .models import Recommendation


def _can_manage_recommendation(user, recommendation):
    """작성자 본인 또는 관리자만 수정과 삭제를 허용합니다."""
    return user == recommendation.author or user.is_staff or user.is_superuser


def _build_writer_name(user, is_anonymous):
    """익명 여부에 따라 화면에 표시할 작성자 이름을 만듭니다."""
    if is_anonymous:
        return '익명'

    current_year = timezone.localtime(timezone.now()).year
    return f'{current_year}-{user.student_id}'


@login_required
def create_recommendation(request):
    """로그인한 학생의 추천글 작성을 처리합니다."""
    if request.method == 'POST':
        form = RecommendationForm(request.POST)
        if form.is_valid():
            recommendation = form.save(commit=False)
            recommendation.author = request.user
            recommendation.writer_name = _build_writer_name(
                request.user,
                recommendation.is_anonymous,
            )
            recommendation.save()
            return redirect('recommendation_list')
    else:
        form = RecommendationForm()

    return render(request, 'recommendations/create.html', {'form': form})


def recommendation_list(request):
    """추천글을 최신순으로 보여줍니다."""
    recommendations = Recommendation.objects.select_related('author').all()
    return render(
        request,
        'recommendations/list.html',
        {'recommendations': recommendations},
    )


def recommendation_detail(request, id):
    """추천글 상세 내용과 댓글 목록을 보여주고 댓글 작성을 처리합니다."""
    recommendation = get_object_or_404(
        Recommendation.objects.select_related('author'),
        id=id,
    )

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')

        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.recommendation = recommendation
            comment.author = request.user
            comment.writer_name = _build_writer_name(
                request.user,
                comment.is_anonymous,
            )
            comment.save()
            return redirect('recommendation_detail', id=recommendation.id)
    else:
        comment_form = CommentForm()

    comments = recommendation.comments.select_related('author').all()

    return render(
        request,
        'recommendations/detail.html',
        {
            'recommendation': recommendation,
            'comments': comments,
            'comment_form': comment_form,
        },
    )


@login_required
def update_recommendation(request, id):
    """작성자 본인 또는 관리자의 추천글 수정을 처리합니다."""
    recommendation = get_object_or_404(Recommendation, id=id)

    if not _can_manage_recommendation(request.user, recommendation):
        raise PermissionDenied

    if request.method == 'POST':
        form = RecommendationForm(request.POST, instance=recommendation)
        if form.is_valid():
            recommendation = form.save(commit=False)
            recommendation.writer_name = _build_writer_name(
                recommendation.author,
                recommendation.is_anonymous,
            )
            recommendation.save()
            return redirect('recommendation_detail', id=recommendation.id)
    else:
        form = RecommendationForm(instance=recommendation)

    return render(
        request,
        'recommendations/edit.html',
        {'form': form, 'recommendation': recommendation},
    )


@login_required
def delete_recommendation(request, id):
    """작성자 본인 또는 관리자의 추천글 삭제를 처리합니다."""
    recommendation = get_object_or_404(Recommendation, id=id)

    if not _can_manage_recommendation(request.user, recommendation):
        raise PermissionDenied

    if request.method == 'POST':
        recommendation.delete()
        return redirect('recommendation_list')

    return render(
        request,
        'recommendations/delete.html',
        {'recommendation': recommendation},
    )
