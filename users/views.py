from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render

from brief_reviews.models import BookQuote
from recommendations.models import Comment, Recommendation

from .forms import LoginForm, SignupForm


@login_required
def home(request):
    """로그인한 학생에게 보여주는 메인 화면입니다."""
    search_query = request.GET.get('q', '').strip()
    recommendations = Recommendation.objects.select_related('author').order_by('-created_at')
    quotes = BookQuote.objects.select_related('author').order_by('-created_at')[:5]

    if search_query:
        recommendations = recommendations.filter(
            Q(book_title__icontains=search_query)
            | Q(book_author__icontains=search_query)
            | Q(post_text__icontains=search_query)
        )

    return render(
        request,
        'users/home.html',
        {
            'recommendations': recommendations,
            'quotes': quotes,
            'search_query': search_query,
        },
    )


@login_required
def mypage_view(request):
    """로그인한 사용자의 마이페이지를 보여줍니다."""
    user = request.user
    
    # 내가 작성한 추천글
    my_recommendations = Recommendation.objects.filter(author=user).order_by('-created_at')
    
    # 내가 작성한 댓글
    my_comments = Comment.objects.filter(
        author=user
    ).select_related('recommendation').order_by('-created_at')
    
    # 내가 작성한 책 한 줄
    my_quotes = BookQuote.objects.filter(author=user).order_by('-created_at')
    
    # 좋아요한 추천글
    liked_recommendations = user.liked_recommendations.all().order_by('-created_at')
    
    return render(
        request,
        'users/mypage.html',
        {
            'my_recommendations': my_recommendations,
            'my_comments': my_comments,
            'my_quotes': my_quotes,
            'liked_recommendations': liked_recommendations,
        },
    )


def signup_view(request):
    """회원가입 화면과 가입 처리를 담당합니다."""
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()

    return render(request, 'users/signup.html', {'form': form})


def login_view(request):
    """학번 기반 로그인 화면과 인증 처리를 담당합니다."""
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    """현재 로그인한 사용자를 로그아웃합니다."""
    logout(request)
    return redirect('login')
