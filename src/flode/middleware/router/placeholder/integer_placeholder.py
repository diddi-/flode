from flode.middleware.router.placeholder.string_placeholder import StringPlaceholder


class IntegerPlaceholder(StringPlaceholder):
    def matches(self, value: str) -> bool:
        try:
            int(value)
            return True
        except ValueError:
            return False
