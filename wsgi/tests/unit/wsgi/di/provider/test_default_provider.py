from unittest import TestCase

from wsgi.di.provider.default_provider import DefaultProvider


class TestDefaultProvider(TestCase):

    def test_new_instance_is_returned_each_time_the_service_is_instantiated(self) -> None:
        class MyClass: pass
        provider = DefaultProvider[MyClass](MyClass, MyClass)
        instance1 = provider.instantiate([], {})
        instance2 = provider.instantiate([], {})
        self.assertNotEqual(instance1, instance2)
