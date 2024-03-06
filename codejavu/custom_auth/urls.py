from django.urls import path
from .views import login_view, registration_view, token_refresh_view, token_blacklist_view


urlpatterns = [
    path('login', login_view, name='login'),
    path('signup', registration_view, name='registration'),
    path('refresh', token_refresh_view, name='token_refresh'),
    path('logout', token_blacklist_view, name='token_logout'),
]
