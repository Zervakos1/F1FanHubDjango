import json

from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from catalog.models import Product
from .models import Review


@require_POST
@login_required
def ajax_review(request, product_id):
    # Save or update one review per user for the selected product.
    product = get_object_or_404(Product, id=product_id)

    data = json.loads(request.body)
    rating = int(data.get("rating", 0))
    comment = data.get("comment", "").strip()

    if rating < 1 or rating > 5:
        return JsonResponse(
            {
                "success": False,
                "message": "Rating must be between 1 and 5.",
            },
            status=400,
        )

    review, created = Review.objects.update_or_create(
        product=product,
        user=request.user,
        defaults={
            "rating": rating,
            "comment": comment,
        },
    )

    avg_rating = product.reviews.aggregate(avg=Avg("rating"))["avg"] or 0
    review_count = product.reviews.count()

    return JsonResponse(
        {
            "success": True,
            "message": "Review saved successfully.",
            "average_rating": round(avg_rating, 1),
            "review_count": review_count,
            "your_rating": review.rating,
            "your_comment": review.comment,
            "created": created,
            "user_id": request.user.id,
            "username": request.user.username,
        }
    )