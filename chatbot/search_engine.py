import re
import difflib

from django.db.models import Q

from products.models import Product
from categories.models import Category


class QueryParser:

    STOP_WORDS = {
        "toi", "tôi", "muon", "muốn", "can", "cần",
        "cho", "xin", "voi", "với", "hay", "hoac",
        "hoặc", "la", "là", "co", "có", "khong",
        "không", "giup", "giúp", "tim", "tìm",
        "san", "pham", "sản", "phẩm", "shop",
        "website", "minh", "mình", "ban", "bạn",
        "mot", "một", "cua", "của", "de", "để",
        "loai", "loại"
    }

    @classmethod
    def normalize(cls, text):
        return text.lower().strip()

    @classmethod
    def keywords(cls, text):

        words = re.findall(
            r"\w+",
            cls.normalize(text)
        )

        return [
            word
            for word in words
            if len(word) > 1
            and word not in cls.STOP_WORDS
        ]

    @staticmethod
    def extract_price(message):

        msg = message.lower()

        m = re.search(r"dưới\s+(\d+)", msg)

        if m:
            return {
                "type": "max",
                "price": int(m.group(1)) * 1000000,
            }

        m = re.search(r"trên\s+(\d+)", msg)

        if m:
            return {
                "type": "min",
                "price": int(m.group(1)) * 1000000,
            }

        m = re.search(r"(\d+)\s*-\s*(\d+)", msg)

        if m:
            return {
                "type": "range",
                "min": int(m.group(1)) * 1000000,
                "max": int(m.group(2)) * 1000000,
            }

        return None


class SearchEngine:

    def __init__(self):

        self.queryset = Product.objects.filter(
            is_active=True
        ).select_related("category")

    def score_product(self, product, keywords):

        score = 0

        name = product.name.lower()
        category = product.category.name.lower()
        description = (product.description or "").lower()

        for word in keywords:

            if word == name:
                score += 100
            elif word in name:
                score += 35

            if word == category:
                score += 60
            elif word in category:
                score += 20

            if word in description:
                score += 10

        return score

    def filter_category(self, message):

        msg = message.lower()

        for category in Category.objects.all():

            if (
                category.name.lower() in msg
                or category.slug.lower() in msg
            ):
                self.queryset = self.queryset.filter(
                    category=category
                )
                return True

        return False

    def filter_price(self, message):

        price = QueryParser.extract_price(message)

        if not price:
            return False

        if price["type"] == "max":

            self.queryset = self.queryset.filter(
                price__lte=price["price"]
            )

        elif price["type"] == "min":

            self.queryset = self.queryset.filter(
                price__gte=price["price"]
            )

        else:

            self.queryset = self.queryset.filter(
                price__gte=price["min"],
                price__lte=price["max"]
            )

        return True
    def filter_keywords(self, message):

        keywords = QueryParser.keywords(message)

        if not keywords:
            return []

        products = list(self.queryset)

        scored = []

        for product in products:

            score = 0

            name = product.name.lower()
            category = product.category.name.lower()
            description = (product.description or "").lower()

            for word in keywords:

                # Tên sản phẩm
                if word == name:
                    score += 100
                elif word in name:
                    score += 40

                # Danh mục
                if word == category:
                    score += 60
                elif word in category:
                    score += 25

                # Mô tả
                if word in description:
                    score += 12

            matched = sum(
                1
                for word in keywords
                if word in (name + " " + category + " " + description)
            )

            score += matched * 15

            if score > 0:
                scored.append((score, product))

        if scored:

            scored.sort(
                key=lambda x: x[0],
                reverse=True
            )

            return [
                product
                for _, product in scored
            ]

        # ===== Fuzzy Search =====

        product_names = list(
            Product.objects.values_list(
                "name",
                flat=True
            )
        )

        matched = []

        for word in keywords:

            matched.extend(

                difflib.get_close_matches(
                    word,
                    product_names,
                    n=10,
                    cutoff=0.5
                )

            )

        if matched:

            return list(

                Product.objects.filter(
                    name__in=matched,
                    is_active=True
                ).select_related("category")

            )

        return []
    def filter_stock(self, message):

        msg = message.lower()

        if any(
            x in msg
            for x in [
                "còn hàng",
                "có hàng",
                "available",
                "in stock",
            ]
        ):

            self.queryset = self.queryset.filter(
                stock__gt=0
            )

            return True

        return False

    def search(self, message):

        found = False

        if self.filter_category(message):
            found = True

        if self.filter_price(message):
            found = True

        if self.filter_stock(message):
            found = True

        products = self.filter_keywords(message)

        if products:
            return products[:10], True

        if found:
            return list(self.queryset[:10]), True

        return [], False


class ProductFormatter:

    @staticmethod
    def build_context(products):

        if not products:
            return "Không tìm thấy sản phẩm phù hợp trong cơ sở dữ liệu."

        lines = []

        for i, product in enumerate(products, 1):

            description = (product.description or "").strip()

            if len(description) > 250:
                description = description[:250] + "..."

            lines.append(
                f"""
Sản phẩm {i}

Tên: {product.name}

Danh mục: {product.category.name}

Giá (CHÍNH XÁC): {int(product.price):,} VNĐ

Tồn kho: {"Còn hàng" if product.stock > 0 else "Hết hàng"}

Mô tả:
{description}
""".strip()
            )

        return "\n\n------------------------\n\n".join(lines)