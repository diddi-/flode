from unittest import TestCase

from flode.di.provider.instance_provider import InstanceProvider


class TestInstanceProvider(TestCase):

    def test_same_instance_is_returned_when_instantiating_multiple_times(self) -> None:
        class MyClass: pass

        instance0 = MyClass()
        provider = InstanceProvider[MyClass](MyClass, MyClass, instance0)
        instance1 = provider.instantiate([], {})
        instance2 = provider.instantiate([], {})
        self.assertEqual(instance0, instance1)
        self.assertEqual(instance0, instance2)
