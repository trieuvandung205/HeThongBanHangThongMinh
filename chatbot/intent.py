import re


class IntentClassifier:
    """
    Phân loại ý định của người dùng.
    """

    RULES = {

        "greeting": [
            "xin chào",
            "chào",
            "hello",
            "hi",
            "hey",
        ],

        "goodbye": [
            "tạm biệt",
            "bye",
            "goodbye",
        ],

        "thanks": [
            "cảm ơn",
            "thank",
            "thanks",
        ],

        "compare": [
            "so sánh",
            "khác nhau",
            "điểm khác",
            "đối chiếu",
        ],

        "recommend": [
            "gợi ý",
            "tư vấn",
            "đề xuất",
            "phù hợp",
            "nên mua",
        ],

        "price": [
            "giá",
            "bao nhiêu",
            "bao tiền",
            "mấy tiền",
        ],

        "stock": [
            "còn hàng",
            "hết hàng",
            "tồn kho",
            "số lượng",
        ],

        "website": [
            "đăng nhập",
            "đăng ký",
            "giỏ hàng",
            "thanh toán",
            "đặt hàng",
            "đơn hàng",
            "tài khoản",
            "đổi mật khẩu",
            "quên mật khẩu",
            "ship",
            "vận chuyển",
        ],

        "cart": [
            "mua",
            "thêm vào giỏ",
            "thêm giỏ",
            "đặt mua",
        ],

        "search": [
            "tìm",
            "xem",
            "có",
            "bán",
            "laptop",
            "máy tính",
            "pc",
            "chuột",
            "bàn phím",
            "tai nghe",
            "loa",
            "màn hình",
            "webcam",
            "ssd",
            "ram",
        ],

        "general": [
            "là gì",
            "giải thích",
            "hướng dẫn",
        ],
    }

    @classmethod
    def classify(cls, message):

        msg = message.lower().strip()

        # So sánh
        if (
            "so sánh" in msg
            or "khác nhau" in msg
            or "điểm khác" in msg
        ):
            return "compare"

        # Tư vấn theo giá
        if re.search(r"dưới\s+\d+", msg):
            return "recommend"

        if re.search(r"trên\s+\d+", msg):
            return "recommend"

        if re.search(r"\d+\s*-\s*\d+", msg):
            return "recommend"

        # Tư vấn
        for word in cls.RULES["recommend"]:
            if word in msg:
                return "recommend"

        # Website
        for word in cls.RULES["website"]:
            if word in msg:
                return "website"

        # Giá
        for word in cls.RULES["price"]:
            if word in msg:
                return "price"

        # Tồn kho
        for word in cls.RULES["stock"]:
            if word in msg:
                return "stock"

        # Tìm kiếm
        for word in cls.RULES["search"]:
            if word in msg:
                return "search"

        # Chào hỏi
        for word in cls.RULES["greeting"]:
            if word in msg:
                return "greeting"

        # Cảm ơn
        for word in cls.RULES["thanks"]:
            if word in msg:
                return "thanks"

        # Tạm biệt
        for word in cls.RULES["goodbye"]:
            if word in msg:
                return "goodbye"

        return "general"