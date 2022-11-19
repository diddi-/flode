from unittest import TestCase

from flode.di.provider.lifetime import Lifetime


class TestLifetime(TestCase):
    def test_is_none(self) -> None:
        self.assertTrue(Lifetime.NONE.is_none())

    def test_is_session(self) -> None:
        self.assertTrue(Lifetime.SESSION.is_session())

    def test_is_singleton(self) -> None:
        self.assertTrue(Lifetime.SINGLETON.is_singleton())
