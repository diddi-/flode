from unittest import TestCase

from flode.middleware.router.exceptions.invalid_path_exception import InvalidPathException
from flode.middleware.router.url_path import UrlPath


class TestUrlPath(TestCase):
    def test_path_must_begin_with_slash(self) -> None:
        with self.assertRaises(InvalidPathException) as err:
            UrlPath("user/profile")
        self.assertIn("must begin with a '/'", str(err.exception))

    def test_path_cant_end_with_slash(self) -> None:
        with self.assertRaises(InvalidPathException) as err:
            UrlPath("/user/")
        self.assertIn("can't end with a '/'", str(err.exception))

    def test_invalid_characters_are_not_allowed(self) -> None:
        with self.assertRaises(InvalidPathException) as err:
            UrlPath("/user/)(¤/profile")
        self.assertIn("is not a valid URL path", str(err.exception))

    def test_original_path_is_returned_when_cast_to_string(self) -> None:
        expected_path = "/user/1/profile"
        path = UrlPath(expected_path)
        self.assertEqual(expected_path, str(path))

    def test_path_can_be_indexed_to_return_requested_part_of_the_path(self) -> None:
        path = UrlPath("/user/1/profile")
        self.assertEqual(3, len(path))
        self.assertEqual("user", path[0])
        self.assertEqual("1", path[1])
        self.assertEqual("profile", path[2])

    def test_path_can_contain_single_slash(self) -> None:
        self.assertEqual("/", str(UrlPath("/")))
