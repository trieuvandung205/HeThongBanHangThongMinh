from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from .models import Product
from categories.models import Category
from django.http import JsonResponse
from itertools import combinations
import re

def home(request):

    categories = Category.objects.all().order_by("name")

    latest_products = (
        Product.objects.filter(is_active=True)
        .select_related("category")
        .order_by("-created_at")[:8]
    )

    featured_products = (
        Product.objects.filter(
            is_active=True,
            stock__gt=0,
        )
        .select_related("category")
        .order_by("-id")[:8]
    )

    return render(
        request,
        "home/index.html",
        {
            "categories": categories,
            "latest_products": latest_products,
            "featured_products": featured_products,
        },
    )


def product_list(request):

    products = (
        Product.objects.filter(is_active=True)
        .select_related("category")
        .order_by("-created_at")
    )

    categories = Category.objects.all().order_by("name")

    return render(
        request,
        "home/product_list.html",
        {
            "products": products,
            "categories": categories,
        },
    )


def category(request, pk):

    category = get_object_or_404(
        Category,
        pk=pk,
    )

    products = (
        Product.objects.filter(
            category=category,
            is_active=True,
        )
        .select_related("category")
        .order_by("-created_at")
    )

    return render(
        request,
        "home/category.html",
        {
            "category": category,
            "products": products,
        },
    )

def search(request):

    keyword = request.GET.get("q", "").strip().lower()

    products = Product.objects.filter(is_active=True)

    synonyms = {
        "máy tính": ["laptop", "notebook", "pc"],
        "laptop": ["máy tính", "notebook", "pc"],
        "pc": ["máy tính", "laptop"],

        "mũ": ["nón", "cap"],
        "nón": ["mũ", "cap"],

        "áo": ["shirt", "thun"],
        "quần": ["pants"],

        "điện thoại": ["phone", "smartphone", "iphone", "android"],
        "phone": ["điện thoại"],

        "tai nghe": ["headphone", "earphone"],
        "headphone": ["tai nghe"],

        "chuột": ["mouse"],
        "mouse": ["chuột"],

        "bàn phím": ["keyboard"],
        "keyboard": ["bàn phím"],

        "sữa": ["vinamilk", "fami", "milo", "ensure"],
    }

    keywords = [keyword]

    if keyword in synonyms:
        keywords.extend(synonyms[keyword])

    query = Q()

    for word in keywords:
        query |= (
            Q(name__icontains=word)
            | Q(description__icontains=word)
            | Q(category__name__icontains=word)
        )

    products = (
        products.filter(query)
        .distinct()
        .select_related("category")
        .order_by("-created_at")
    )

    return render(
        request,
        "home/search.html",
        {
            "keyword": keyword,
            "products": products,
        },
    )

def product_detail(request, slug):

    product = get_object_or_404(
        Product,
        slug=slug,
        is_active=True,
    )

    related_products = (
        Product.objects.filter(
            category=product.category,
            is_active=True,
        )
        .exclude(id=product.id)[:4]
    )

    return render(
        request,
        "products/product_detail.html",
        {
            "product": product,
            "related_products": related_products,
        },
    )
def search_suggest(request):

    q = request.GET.get("q", "").strip().lower()

    if not q:
        return JsonResponse([], safe=False)

    products = Product.objects.filter(
        is_active=True
    ).select_related("category")

    suggestions = {}

    for product in products:

        words = re.findall(
            r"\w+",
            product.name.lower()
        )

        # Tự sinh từ khóa
        for size in range(1, min(4, len(words)) + 1):

            for combo in combinations(words, size):

                phrase = " ".join(combo)

                if q in phrase:

                    suggestions[phrase] = {
                        "type": "keyword",
                        "text": phrase
                    }

        # Gợi ý sản phẩm
        if q in product.name.lower():

            suggestions[product.name] = {
                "type": "product",
                "name": product.name,
                "url": f"/product/{product.slug}/"
            }

    data = list(suggestions.values())

    # Keyword lên trước
    data.sort(
        key=lambda x: (
            x["type"] != "keyword",
            len(
                x.get("text", x.get("name", ""))
            )
        )
    )

    return JsonResponse(
        data[:15],
        safe=False
    )