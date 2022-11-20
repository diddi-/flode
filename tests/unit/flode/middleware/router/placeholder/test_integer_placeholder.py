from unittest import TestCase

from flode.middleware.router.placeholder.integer_placeholder import IntegerPlaceholder


class TestIntegerPlaceholder(TestCase):
    def test_integers_match(self) -> None:
        self.assertTrue(IntegerPlaceholder("age", 0).matches("1"))

    def test_string_characters_do_not_match(self) -> None:
        self.assertFalse(IntegerPlaceholder("age", 0).matches("nomatch"))

    def test_float_do_not_match(self) -> None:
        self.assertFalse(IntegerPlaceholder("age", 0).matches("3.14"))
