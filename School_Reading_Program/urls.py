from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('brief-reviews/', include('brief_reviews.urls')),
    path('recommendations/', include('recommendations.urls')),
    path('', include('users.urls')),
]
