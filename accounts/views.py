from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone

from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import PremiumSubscription, DiscountReward, RaffleEntry

def sync_user_premium_role(user):
    has_active_subscription = user.premium_subscriptions.filter(is_active=True).exists()
    user.profile.role = 'premium' if has_active_subscription else 'user'
    user.profile.save()

def user_has_premium_access(user):
    if user.is_superuser:
        return True
    return user.premium_subscriptions.filter(is_active=True).exists()
    

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
            )

            user.profile.phone = form.cleaned_data.get('phone', '')
            user.profile.country = form.cleaned_data.get('country', '')
            user.profile.save()

            login(request, user)
            return redirect('dashboard-router')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            request.session.set_expiry(0)
            return redirect('dashboard-router')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('public-dashboard')

@login_required
def upgrade_premium_view(request):
    if request.user.is_superuser:
        messages.info(request, 'Admin users already have full access.')
        return redirect('admin-dashboard')

    if request.method == 'POST':
        has_active_subscription = request.user.premium_subscriptions.filter(is_active=True).exists()

        if has_active_subscription:
            sync_user_premium_role(request.user)
            messages.info(request, 'Your account is already premium.')
            return redirect('premium-dashboard')

        PremiumSubscription.objects.create(
            user=request.user,
            plan_name='Premium Membership',
            price=15.00,
            is_active=True
        )

        sync_user_premium_role(request.user)

        messages.success(request, 'Premium membership activated successfully for $15 (simulated).')
        return redirect('premium-dashboard')

    return render(request, 'accounts/upgrade_premium.html')


@login_required
def cancel_premium_view(request):
    if request.user.is_superuser:
        messages.info(request, 'Admin users cannot cancel admin access.')
        return redirect('admin-dashboard')

    active_subscriptions = request.user.premium_subscriptions.filter(is_active=True)

    if not active_subscriptions.exists():
        sync_user_premium_role(request.user)
        messages.info(request, 'You do not have an active premium subscription.')
        return redirect('user-dashboard')

    if request.method == 'POST':
        active_subscriptions.update(
            is_active=False,
            ended_at=timezone.now()
        )

        sync_user_premium_role(request.user)

        messages.success(request, 'Premium membership cancelled successfully.')
        return redirect('user-dashboard')

    return render(request, 'accounts/cancel_premium.html')

@login_required
def profile_view(request):
    user_form = UserUpdateForm(instance=request.user)
    profile_form = ProfileUpdateForm(instance=request.user.profile)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'profile/profile.html', context)

@login_required
def redeem_discount_view(request):
    if request.user.is_superuser:
        messages.info(request, 'Admin users do not need discount rewards.')
        return redirect('admin-dashboard')

    sync_user_premium_role(request.user)

    if not user_has_premium_access(request.user):
        messages.info(request, 'Only users with an active premium subscription can redeem reward points.')
        return redirect('user-dashboard')

    if request.method == 'POST':
        if request.user.profile.premium_points < 200:
            messages.error(request, 'You need at least 200 points to redeem a €10 discount.')
            return redirect('premium-dashboard')

        request.user.profile.premium_points -= 200
        request.user.profile.save()

        DiscountReward.objects.create(
            user=request.user,
            name='€10 Discount Voucher',
            points_cost=200,
            discount_amount=10.00,
            is_used=False
        )

        messages.success(request, '€10 discount reward redeemed successfully.')
        return redirect('premium-dashboard')

    return redirect('premium-dashboard')


@login_required
def join_raffle_view(request):
    if request.user.is_superuser:
        messages.info(request, 'Admin users do not need raffle entry.')
        return redirect('admin-dashboard')

    sync_user_premium_role(request.user)

    if not user_has_premium_access(request.user):
        messages.info(request, 'Only users with an active premium subscription can join the raffle.')
        return redirect('user-dashboard')

    if request.method == 'POST':
        if request.user.profile.premium_points < 100:
            messages.error(request, 'You need at least 100 points to join the raffle.')
            return redirect('premium-dashboard')

        request.user.profile.premium_points -= 100
        request.user.profile.save()

        RaffleEntry.objects.create(
            user=request.user,
            prize_name='Free Race Ticket Raffle',
            points_cost=100,
            status='joined'
        )

        messages.success(request, 'You joined the free ticket raffle successfully.')
        return redirect('premium-dashboard')

    return redirect('premium-dashboard')