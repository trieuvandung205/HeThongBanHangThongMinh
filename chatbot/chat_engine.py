from .search_engine import SearchEngine, ProductFormatter
from .ai_service import ask_ai


class ChatEngine:

    SESSION_KEY = "chatbot_state"

    def __init__(self, session):

        self.session = session

        self.state = session.get(
            self.SESSION_KEY,
            {
                "history": [],
                "last_query": "",
                "last_products": [],
            },
        )

    def save(self):

        self.session[self.SESSION_KEY] = self.state
        self.session.modified = True

    def add_history(self, role, message):

        self.state["history"].append(
            {
                "role": role,
                "content": message,
            }
        )

        if len(self.state["history"]) > 12:
            self.state["history"] = self.state["history"][-12:]

    def build_state(self, message, products):

        return {
            "question": message,
            "history": self.state["history"],
            "products": ProductFormatter.build_context(products),
        }

    def handle(self, message):

        self.add_history("user", message)

        engine = SearchEngine()

        products, found = engine.search(message)

        state = self.build_state(
            message,
            products
        )

        reply = ask_ai(state)

        self.add_history(
            "assistant",
            reply,
        )

        self.state["last_query"] = message
        self.state["last_products"] = [
            p.id for p in products
        ]

        self.save()

        return reply, products