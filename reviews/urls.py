from django.urls import path
from .views import ajax_review

app_name = "reviews"

urlpatterns = [
    path('ajax/<int:product_id>/', ajax_review, name='ajax-review'),
]