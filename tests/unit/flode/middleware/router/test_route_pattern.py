from unittest import TestCase

from flode.middleware.router.exceptions.invalid_route_pattern_exception import InvalidRoutePatternException
from flode.middleware.router.placeholder.integer_placeholder import IntegerPlaceholder
from flode.middleware.router.placeholder.string_placeholder import StringPlaceholder
from flode.middleware.router.route_pattern import RoutePattern
from flode.middleware.router.url_path import UrlPath


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

    def test_special_characters_are_not_allowed_in_pattern(self) -> None:
        with self.assertRaises(InvalidRoutePatternException) as err:
            RoutePattern("/user/%#/profile")

        self.assertIn("is not a valid route pattern", str(err.exception))

    def test_route_patterns_must_start_with_a_slash(self) -> None:
        with self.assertRaises(InvalidRoutePatternException) as err:
            RoutePattern("user/profile")
        self.assertIn("must begin with a '/'", str(err.exception))

    def test_route_patterns_cant_end_with_slash(self) -> None:
        with self.assertRaises(InvalidRoutePatternException) as err:
            RoutePattern("/user/")
        self.assertIn("can't end with a '/'", str(err.exception))

    def test_route_patterns_can_be_matched_against_url_paths(self) -> None:
        path = UrlPath("/user/1/profile")
        self.assertTrue(RoutePattern(str(path)).matches(path), "Route pattern matches string")

    def test_route_patterns_can_have_placeholders(self) -> None:
        pattern = RoutePattern("/user/<id>/profile")
        self.assertTrue(pattern.matches(UrlPath("/user/1/profile")), "Route pattern matches string")

    def test_single_slash_route_patterns_are_allowed(self) -> None:
        self.assertEqual("/", str(RoutePattern("/")))

    def test_single_slash_route_pattern_can_be_appended_to_another_route_pattern(self) -> None:
        pattern1 = RoutePattern("/user")
        pattern2 = RoutePattern("/")
        expected_pattern = RoutePattern("/user")

        self.assertEqual(expected_pattern, pattern1 + pattern2)

    def test_route_pattern_can_be_appended_to_a_single_slash_pattern(self) -> None:
        pattern1 = RoutePattern("/")
        pattern2 = RoutePattern("/user")
        expected_pattern = RoutePattern("/user")

        self.assertEqual(expected_pattern, pattern1 + pattern2)

    def test_placeholders_are_returned_in_the_order_they_are_defined_in_the_pattern(self) -> None:
        pattern = RoutePattern("/<id>/<name>/<age>/<query>")
        expected_placeholders = ["id", "name", "age", "query"]
        self.assertEqual(expected_placeholders, [p.name for p in pattern.get_placeholders()])

    def test_placeholders_are_created_correctly(self) -> None:
        pattern = RoutePattern("/user/<name: str>/<age: int>")
        expected_placeholders = [StringPlaceholder("name", 1), IntegerPlaceholder("age", 2)]
        self.assertEqual(expected_placeholders, pattern.get_placeholders())

    def test_two_single_slashes_can_be_appended_to_create_one_single_slash(self) -> None:
        pattern = RoutePattern("/")
        expected_pattern = RoutePattern("/")
        self.assertEqual(expected_pattern, pattern + pattern)
