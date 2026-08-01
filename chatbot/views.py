import json
import traceback

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .chat_engine import ChatEngine


@require_POST
def ask(request):

    try:
        data = json.loads(request.body)

    except json.JSONDecodeError:

        return JsonResponse(
            {
                "success": False,
                "reply": "Dữ liệu không hợp lệ."
            },
            status=400
        )

    message = data.get("message", "").strip()

    if not message:

        return JsonResponse(
            {
                "success": False,
                "reply": "Bạn chưa nhập câu hỏi."
            },
            status=400
        )

    try:

        engine = ChatEngine(request.session)

        reply, products = engine.handle(message)

        product_list = []

        for p in products:

            product_list.append({
                "id": p.id,
                "name": p.name,
                "slug": p.slug,
                "price": int(p.price),
                "stock": p.stock,
                "image": p.image.url if p.image else "",
                "category": p.category.name,
            })

        return JsonResponse({
            "success": True,
            "reply": reply,
            "products": product_list,
        })

    except Exception:

        traceback.print_exc()

        return JsonResponse(
            {
                "success": False,
                "reply": "Đã xảy ra lỗi khi xử lý AI."
            },
            status=500
        )