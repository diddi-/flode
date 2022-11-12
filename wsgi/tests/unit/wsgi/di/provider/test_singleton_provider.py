from unittest import TestCase

from wsgi.di.provider.singleton_provider import SingletonProvider


class TestSingletonProvider(TestCase):

    def test_same_instance_is_returned_when_instantiating_multiple_times(self) -> None:
        class MyClass: pass
        provider = SingletonProvider[MyClass](MyClass, MyClass)
        instance1 = provider.instantiate([], {})
        instance2 = provider.instantiate([], {})
        self.assertEqual(instance1, instance2)
