from django.urls import path
from .views import (
    register_view,
    login_view,
    logout_view,
    upgrade_premium_view,
    cancel_premium_view,
    profile_view,
    redeem_discount_view,
    join_raffle_view,
)

app_name = "accounts"

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('upgrade/', upgrade_premium_view, name='upgrade-premium'),
    path('cancel-premium/', cancel_premium_view, name='cancel-premium'),
    path('profile/', profile_view, name='profile'),
    path('redeem-discount/', redeem_discount_view, name='redeem-discount'),
    path('join-raffle/', join_raffle_view, name='join-raffle'),
]