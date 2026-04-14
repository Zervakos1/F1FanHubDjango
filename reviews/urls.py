from django.urls import path
from .views import ajax_review

urlpatterns = [
    path('ajax/<int:product_id>/', ajax_review, name='ajax-review'),
]