from unittest import TestCase

from flode.middleware.router.exceptions.invalid_route_pattern_exception import InvalidRoutePatternException
from flode.middleware.router.route_pattern import RoutePattern


class TestRoutePattern(TestCase):
    def test_pattern_can_be_stringified(self) -> None:
        expected_string = "/admin"
        pattern = RoutePattern(expected_string)
        self.assertEqual(expected_string, str(pattern))

    def test_two_patterns_are_equal_when_the_pattern_are_the_same(self) -> None:
        path = "/user/profile"
        pattern1 = RoutePattern(path)
        pattern2 = RoutePattern(path)
        self.assertEqual(pattern1, pattern2)

    def test_two_patterns_can_be_added_together_to_form_a_new_concatenated_pattern(self) -> None:
        expected_path = "/user/profile"
        pattern1 = RoutePattern("/user")
        pattern2 = RoutePattern("/profile")
        self.assertEqual(expected_path, str(pattern1 + pattern2))

    def test_trailing_slashes_are_removed_from_pattern(self) -> None:
        pattern = RoutePattern("/user/")
        self.assertEqual("/user", str(pattern))

    def test_special_characters_are_not_allowed_in_pattern(self) -> None:
        with self.assertRaises(InvalidRoutePatternException):
            RoutePattern("/user/%#/profile")
